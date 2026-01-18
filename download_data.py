import requests
import pandas as pd
import numpy as np
import os

URLS = [
    "https://raw.githubusercontent.com/wadefagen/datasets/master/housing-prices/train.csv",
    "https://raw.githubusercontent.com/dgawlik/househunter/master/data/train.csv",
    "https://raw.githubusercontent.com/emanhamed/Houses-dataset/master/Houses%20Dataset/HousesInfo.txt", # Might be different
    "https://raw.githubusercontent.com/Shreyas3108/house-price-prediction/master/KC_Housing_Data/kc_house_data.csv" # Different dataset but fallback
]

# The official kaggle dataset usually has these columns
REQUIRED_COLS = ["OverallQual", "GrLivArea", "TotalBsmtSF", "GarageCars", "BedroomAbvGr", "FullBath", "YearBuilt", "Neighborhood", "SalePrice"]

def download_data():
    for url in URLS:
        try:
            print(f"Trying to download from {url}...")
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # Check if it looks like a CSV and has enough data
                if len(r.content) > 1000:
                    with open('train.csv', 'wb') as f:
                        f.write(r.content)
                    print(f"Downloaded successfully from {url}")
                    
                    # Verify columns
                    try:
                        df = pd.read_csv('train.csv')
                        missing = [c for c in REQUIRED_COLS if c not in df.columns]
                        if not missing:
                            print("Dataset has all required columns.")
                            return True
                        else:
                            print(f"Dataset missing columns: {missing}")
                    except:
                        print("Failed to parse CSV.")
            else:
                print(f"Failed with status {r.status_code}")
        except Exception as e:
            print(f"Error downloading: {e}")
    return False

def generate_synthetic():
    print("Generating synthetic dataset...")
    n_samples = 1000
    np.random.seed(42)
    
    data = {
        'OverallQual': np.random.randint(1, 11, n_samples),
        'GrLivArea': np.random.randint(500, 4000, n_samples),
        'TotalBsmtSF': np.random.randint(0, 3000, n_samples),
        'GarageCars': np.random.randint(0, 5, n_samples),
        'BedroomAbvGr': np.random.randint(0, 6, n_samples),
        'FullBath': np.random.randint(1, 4, n_samples),
        'YearBuilt': np.random.randint(1900, 2023, n_samples),
        'Neighborhood': np.random.choice(['CollgCr', 'Veenker', 'Crawfor', 'NoRidge', 'Mitchel', 'Somerst', 'NWAmes', 'OldTown', 'BrkSide', 'Sawyer', 'NridgHt', 'NAmes', 'SawyerW', 'IDOTRR', 'MeadowV', 'Edwards', 'Timber', 'Gilbert', 'StoneBr', 'ClearCr', 'NPkVill', 'Blmngtn', 'BrDale', 'SWISU', 'Blueste'], n_samples),
    }
    
    # Simple linear generation for price + noise
    price = (data['OverallQual'] * 20000) + (data['GrLivArea'] * 100) + (data['TotalBsmtSF'] * 50) + (data['GarageCars'] * 10000) + (data['YearBuilt'] * 100)
    data['SalePrice'] = price + np.random.normal(0, 20000, n_samples)
    
    df = pd.DataFrame(data)
    df.to_csv('train.csv', index=False)
    print("Synthetic dataset generated.")

if __name__ == "__main__":
    if not download_data():
        generate_synthetic()
