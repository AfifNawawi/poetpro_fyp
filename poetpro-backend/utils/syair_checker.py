import re
from nltk.tokenize import word_tokenize
from utils.spacy_analyzer import analyze_with_spacy

# -----------------------------
# Helper: extract rhyme unit
# -----------------------------
def get_rhyme_unit(word):
    """
    Syair rhyme rule:
    - If word ends with a vowel → use last vowel only
    - Else → use last 2 characters
    """
    word = re.sub(r"[^\w]", "", word.lower())

    if not word:
        return ""

    if word[-1] in "aeiou":
        return word[-1]          # vowel-ending → 1 char
    else:
        return word[-2:] if len(word) >= 2 else word


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
# Main Syair Analyzer
# -----------------------------
def analyze_syair(text):
    raw_lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Handle comma-separated input
    if len(raw_lines) == 1 and "," in raw_lines[0]:
        lines = [l.strip() for l in raw_lines[0].split(",") if l.strip()]
    else:
        lines = raw_lines

    result = {
        "line_count": len(lines),
        "structure": "Invalid",
        "rhyme_pattern": "Unknown",
        "message": "",
        "tokens_per_line": [],
        "syllables_per_line": [],
        "rhyme_units": [],
        "spacy_analysis": []
    }

    # ❌ Minimum rule
    if len(lines) < 4:
        result["message"] = "Syair requires at least 4 lines."
        result["issue_type"] = "line_count_error"
        return result

    # ✅ Analyze ALL lines (not just first 4)
    for line in lines:
        tokens = word_tokenize(line)
        result["tokens_per_line"].append(tokens)

        result["syllables_per_line"].append(
            sum(count_syllables(w) for w in tokens)
        )

        rhyme = get_rhyme_unit(tokens[-1]) if tokens else ""
        result["rhyme_units"].append(rhyme)

        result["spacy_analysis"].append(analyze_with_spacy(line))

    # -----------------------------
    # Syair rhyme rule: ALL AAAA
    # -----------------------------
    if len(set(result["rhyme_units"])) == 1:
        result["structure"] = "Syair"
        result["rhyme_pattern"] = "AAAA"
        result["message"] = "Syair structure is valid."
        result["issue_type"] = "correct"
    else:
        result["message"] = "Syair must use the same rhyme in all lines."
        result["issue_type"] = "rhyme_error"

    # 🔎 KEEP THESE (as requested)
    print("NLTK TOKENS PER LINE:", result["tokens_per_line"])
    print("SYLLABLES PER LINE:", result["syllables_per_line"])
    print("RHYME UNITS:", result["rhyme_units"])
    print("SPACY ANALYSIS:", result["spacy_analysis"])

    return result












