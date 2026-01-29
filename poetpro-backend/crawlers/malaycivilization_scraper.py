import requests
import time
import pandas as pd
import os
from io import StringIO

# =========================
# CONFIG
# =========================
BASE_URL = "https://www.malaycivilization.com.my/items/browse"
TOTAL_PAGES = 5896     # update if site grows
DELAY = 2.0           # polite crawling

OUTPUT_DIR = "../data/raw"
OUTPUT_FILE = "malaycivilization_raw.csv"

# =========================
# HEADERS (BROWSER EMULATION)
# =========================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.malaycivilization.com.my/items/browse",
    "Connection": "keep-alive"
}

# =========================
# SETUP
# =========================
os.makedirs(OUTPUT_DIR, exist_ok=True)
session = requests.Session()
session.headers.update(HEADERS)

all_rows = []

print("🚀 Starting MalayCivilization bulk downloader...")
print(f"Total pages: {TOTAL_PAGES}")
print("Saving to:", os.path.join(OUTPUT_DIR, OUTPUT_FILE))
print("-" * 60)

# =========================
# DOWNLOAD LOOP
# =========================
for page in range(1, TOTAL_PAGES + 1):
    try:
        url = f"{BASE_URL}?output=csv&page={page}"
        print(f"📥 Downloading page {page}/{TOTAL_PAGES}")

        response = session.get(url, timeout=30)
        response.raise_for_status()

        # Convert CSV content into DataFrame
        df = pd.read_csv(StringIO(response.text))

        if df.empty:
            print(f"⚠ Page {page} returned empty data")
        else:
            all_rows.append(df)

        time.sleep(DELAY)

    except Exception as e:
        print(f"❌ Error on page {page}: {e}")
        time.sleep(5)   # wait longer if blocked
        continue


# =========================
# MERGE & SAVE
# =========================
if not all_rows:
    print("❌ No data downloaded. Something went wrong.")
else:
    full_df = pd.concat(all_rows, ignore_index=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    full_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("\n✅ Download complete!")
    print("Total records:", len(full_df))
    print("Saved to:", output_path)

