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

# location table
def location_table(df):

    location = df[["city","state","country"]].drop_duplicates().copy()

    location = location.dropna()

    # add location id column in loacation data
    location.insert(0, "location_id", range(1, len(location) + 1))

    

    return location

location = location_table(df)

print(location.head())

# skills_table

def skills_table(df):
        
    skills = df[["key_skills"]].dropna().copy()

    # separate every skill in key skill column

    skills["key_skills"] = skills["key_skills"].str.split(",")

    skills = skills.explode("key_skills")

    skills["key_skills"] = skills["key_skills"].str.strip()

    skills = skills.drop_duplicates()
    skills = skills.dropna()
    skills = skills.reset_index(drop=True)

    skills.insert(0, "skill_id", range(1, len(skills) + 1))

    skills = skills.rename(columns={"key_skills": "skill_name"})

    
    return skills

skills= skills_table(df)

print(skills.head())