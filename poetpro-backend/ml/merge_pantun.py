import pandas as pd
import os

MALAY_FILE = r"C:\Users\nawaw\poetpro-backend\data\cleaned\pantun_malaysia.csv"
SAMPIRAN_FILE = r"C:\Users\nawaw\poetpro-backend\data\cleaned\sampiran_clean.csv"

OUTPUT_DIR = r"C:\Users\nawaw\poetpro-backend\data\final"
OUTPUT_FILE = "pantun_full_corpus.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df_malay = pd.read_csv(MALAY_FILE)
df_sampiran = pd.read_csv(SAMPIRAN_FILE)

df_malay["source"] = "MalayCivilization (Malaysia)"
df_sampiran["source"] = "Sampiran Dataset (Indonesia)"

df_malay = df_malay[["pantun", "source"]]
df_sampiran = df_sampiran[["pantun", "source"]]

df_all = pd.concat([df_malay, df_sampiran], ignore_index=True)

df_all.to_csv(os.path.join(OUTPUT_DIR, OUTPUT_FILE), index=False, encoding="utf-8-sig")

print("✅ Pantun corpus merged!")
print("Total pantun:", len(df_all))
print("Saved to:", os.path.join(OUTPUT_DIR, OUTPUT_FILE))
