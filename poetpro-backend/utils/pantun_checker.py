import re
from nltk.tokenize import word_tokenize
from utils.spacy_analyzer import analyze_with_spacy


# -----------------------------
# Helper: extract rhyme unit
# -----------------------------
def get_rhyme_unit(word):
    """
    Pantun rhyme rules:
    - If last character is a vowel → use that vowel
    - Else → use last 2 characters
    """
    word = re.sub(r"[^\w]", "", word.lower())

    if not word:
        return ""

    vowels = "aeiou"

    # If ends with vowel → take only that vowel
    if word[-1] in vowels:
        return word[-1]

    # Else → take last 2 characters
    return word[-2:] if len(word) >= 2 else word


# -----------------------------
# Helper: get last real word
# -----------------------------
def get_last_word(tokens):
    """
    Return last alphabetic word (ignore punctuation)
    """
    for token in reversed(tokens):
        clean = re.sub(r"[^a-zA-Z]", "", token)
        if clean:
            return clean
    return ""


# -----------------------------
# Helper: syllable estimation
# -----------------------------
def count_syllables(word):
    word = re.sub(r"[^a-z]", "", word.lower())
    vowels = "aeiou"
    diphthongs = ["ai", "au", "oi"]

    syllables = 0
    i = 0
    while i < len(word):
        if word[i] in vowels:
            if i + 1 < len(word) and word[i:i+2] in diphthongs:
                syllables += 1
                i += 2
            else:
                syllables += 1
                i += 1
        else:
            i += 1

    return max(1, syllables)


# -----------------------------
# Main Pantun Analyzer
# -----------------------------
def analyze_pantun(text):
    raw_lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Handle comma-separated pantun
    if len(raw_lines) == 1 and "," in raw_lines[0]:
        lines = [l.strip() for l in raw_lines[0].split(",") if l.strip()]
    else:
        lines = raw_lines

    result = {
        "line_count": len(lines),
        "structure": "Invalid",
        "rhyme_pattern": "Unknown",
        "message": "",
        "issue_type": None,
        "tokens_per_line": [],
        "syllables_per_line": [],
        "rhyme_units": [],
        "spacy_analysis": []
    }

    # ❌ Line count error
    if len(lines) != 4:
        result["issue_type"] = "line_count_error"
        result["message"] = "Pantun must have exactly 4 lines."
        return result

    # Analyze each line
    for line in lines:
        tokens = word_tokenize(line)
        result["tokens_per_line"].append(tokens)

        result["syllables_per_line"].append(
            sum(count_syllables(w) for w in tokens)
        )

        # ✅ FIX: get last real word, not punctuation
        last_word = get_last_word(tokens)
        rhyme = get_rhyme_unit(last_word)
        result["rhyme_units"].append(rhyme)

        result["spacy_analysis"].append(analyze_with_spacy(line))

    ru = result["rhyme_units"]

    # ✅ ABAB check
    if ru[0] == ru[2] and ru[1] == ru[3]:
        result["structure"] = "Pantun"
        result["rhyme_pattern"] = "ABAB"
        result["issue_type"] = "correct"
        result["message"] = "Pantun structure is valid."

    elif ru[0] != ru[2] and ru[1] != ru[3]:
        result["issue_type"] = "rhyme_error_line_3_and_4"
        result["message"] = "Third line should rhyme with first line and fourth line should rhyme with second line."

    elif ru[0] != ru[2]:
        result["issue_type"] = "rhyme_error_line_3"
        result["message"] = "Third line should rhyme with first line."

    elif ru[1] != ru[3]:
        result["issue_type"] = "rhyme_error_line_4"
        result["message"] = "Fourth line should rhyme with second line."

    # Debug info (optional)
    print("NLTK TOKENS PER LINE:", result["tokens_per_line"])
    print("SYLLABLES PER LINE:", result["syllables_per_line"])
    print("RHYME UNITS:", result["rhyme_units"])

    return result













