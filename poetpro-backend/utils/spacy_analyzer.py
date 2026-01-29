import spacy

# Load once (important for performance)
nlp = spacy.load("en_core_web_sm")

def analyze_with_spacy(lines):
    """
    Takes list of lines (strings)
    Returns POS tags and dependency info per line
    """
    spacy_result = []

    for line in lines:
        doc = nlp(line)

        spacy_result.append({
            "text": line,
            "tokens": [
                {
                    "text": token.text,
                    "pos": token.pos_,
                    "dep": token.dep_
                }
                for token in doc
            ]
        })

    return spacy_result
