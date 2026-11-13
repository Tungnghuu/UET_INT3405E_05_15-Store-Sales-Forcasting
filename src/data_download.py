import os
import zipfile
import kagglehub

# 1. Download the zip archive
zip_path = kagglehub.competition_download('store-sales-time-series-forecasting')
print("Downloaded zip to:", zip_path)

# 2. Extract all CSVs into your project's data/raw folder
extract_dir = "data/raw"
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("Extracted files:", os.listdir(extract_dir))
