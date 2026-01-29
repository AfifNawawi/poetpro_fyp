import re

INPUT_FILE = r"C:\Users\nawaw\poetpro-backend\data\syair_corpus.txt"
OUTPUT_FILE = r"C:\Users\nawaw\poetpro-backend\data\cleaned\syair_clean.txt"

def clean_text(text):
    text = text.strip()
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

cleaned = clean_text(raw)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(cleaned)

print("✅ Syair corpus cleaned and saved.")
