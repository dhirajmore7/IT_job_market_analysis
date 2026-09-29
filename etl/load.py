import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

from etl.config import db_name,db_password,db_port


# Database connection
conn = create_engine(f"mysql+pymysql://root:{db_password}@localhost:{db_port}/{db_name}")

# Read cleaned data
file_path = Path("processed_data/naukri/naukri_clean_data.csv")
df = pd.read_csv(file_path)

print("Data loaded successfully")
print(df.head())



# 1. COMPANY TABLE
def comapany_table(df):
    company = df[["company"]].drop_duplicates().copy()

    company = company.reset_index(drop=True)
    company.insert(0, "company_id", range(101, 101 + len(company)))

    

    company.dropna(inplace=True)
    
    return company

company = comapany_table(df)
print(company.head())
