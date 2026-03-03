import pandas as pd

DATA_PATH = "data/raw/online_retail.csv"

def ingest_data():
    df = pd.read_csv(DATA_PATH)
    
    print("Data Ingestion Complete")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nColumn Names:")
    print(df.columns.tolist())
    
    print("\nMissing Values per Column:")
    print(df.isnull().sum())

    print("\nSample Rows:")
    print(df.head())

if __name__ == "__main__":
    ingest_data() 