import os
import pandas as pd
import re

RAW_FILE = r"C:\Users\nawaw\poetpro-backend\data\raw\sampiran\sampiran.txt"
OUTPUT_DIR = r"C:\Users\nawaw\poetpro-backend\data\cleaned"
OUTPUT_FILE = "sampiran_clean.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📥 Loading Sampiran raw dataset...")

with open(RAW_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Split by <EOS> (each pantun)
raw_pantun = raw_text.split("<EOS>")

clean_pantun_list = []

for p in raw_pantun:
    p = p.replace("<BOS>", "")
    p = p.replace("<CONTENT>", "\n")
    p = p.replace("<CLS>", "\n")

    # Remove extra spaces
    p = re.sub(r"\n+", "\n", p)
    p = re.sub(r"[ \t]+", " ", p)

    p = p.strip()

    # Keep only real pantun (4 lines)
    lines = [l.strip() for l in p.split("\n") if l.strip()]
    if len(lines) == 4:
        clean_pantun_list.append("\n".join(lines))

print("Total clean pantun:", len(clean_pantun_list))

df = pd.DataFrame({
    "title": [f"Sampiran_{i+1}" for i in range(len(clean_pantun_list))],
    "pantun": clean_pantun_list,
    "source": "Sampiran Dataset (GitHub)"
})

output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n✅ Sampiran dataset cleaned properly!")
print("Saved to:", output_path)

