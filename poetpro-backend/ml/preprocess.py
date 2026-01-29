import pandas as pd
import os
import re
import csv
from html import unescape

RAW_FILE = r"C:\Users\nawaw\poetpro-backend\data\raw\malaycivilization_raw.csv"
OUTPUT_DIR = r"C:\Users\nawaw\poetpro-backend\data\cleaned"
OUTPUT_FILE = "pantun_malaysia.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📥 Loading MalayCivilization archive...")
df = pd.read_csv(RAW_FILE, low_memory=False)

TITLE_COL = "Dublin Core:Title"
DESC_COL = "Dublin Core:Description"
ALT_TEXT_COL = "Item Type Metadata:Text"
COLLECTION_COL = "collection"
TAG_COL = "tags"

pantun_collections = ["Sejuta Pantun", "Pantun Melayu", "Pantun Tradisional"]

df = df[df[COLLECTION_COL].isin(pantun_collections)]
print("After pantun collection filter:", len(df))

def extract_pantun(row):
    parts = []

    for col in [DESC_COL, ALT_TEXT_COL]:
        t = row.get(col)
        if isinstance(t, str) and t.strip():
            parts.append(t)

    if not parts:
        return None

    text = "\n".join(parts)
    text = unescape(text)

    # Convert <br> to newline
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    # Remove remaining HTML
    text = re.sub(r"<.*?>", "", text)

    # Normalize whitespace
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    # Convert real newlines into literal \n for CSV safety
    text = text.strip().replace("\n", "\\n")

    return text

df["pantun"] = df.apply(extract_pantun, axis=1)
df = df[df["pantun"].notna()]

output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# Write using strict CSV writer
with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)

    writer.writerow(["title", "pantun", "tags", "collection"])

    for _, row in df.iterrows():
        writer.writerow([
            row.get(TITLE_COL, ""),
            row["pantun"],
            row.get(TAG_COL, ""),
            row.get(COLLECTION_COL, "")
        ])

print("\n✅ Pantun dataset exported correctly!")
print("Total pantun:", len(df))
print("Saved to:", output_path)








