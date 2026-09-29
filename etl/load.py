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

# jobs table
def jobs_table(df,company,location):
    jobs = df[
        [
            "company",
            "city",
            "state",
            "country",
            "job_title",
            "experience",
            "salary",
            "job_description",
            "job_url"
        ]
    ].copy()

    # Add company ID
    jobs = jobs.merge(company, on="company", how="left")

    # Add location ID
    jobs = jobs.merge(location, on=['city','state','country'], how="left")

    jobs = jobs[
        [
            "company_id",
            "location_id",
            "job_title",
            "experience",
            "salary",
            "job_description",
            "job_url"
        ]
    ]

    jobs = jobs.drop_duplicates(subset=["job_url"])

    

    return jobs

jobs = jobs_table(df,company,location)

print(jobs.head())




def job_skills_bridge(df,jobs,skills):
    
    jobs.index=range(1,1+len(jobs))

    job_skills = df[["job_url", "key_skills"]].copy()


    # Separate each skill

    job_skills["key_skills"] = job_skills["key_skills"].str.split(",")

    job_skills = job_skills.explode("key_skills")

    job_skills["key_skills"] = job_skills["key_skills"].str.strip()

    # Add job ID using job URL
    job_skills = job_skills.merge( jobs[["job_url"]].reset_index().rename(columns={"index": "job_id"}),  on="job_url", how="left")

    print(job_skills)

    # Add skill ID
    job_skills = job_skills.merge( skills, left_on="key_skills", right_on="skill_name", how="left")

    job_skills = job_skills[["job_id", "skill_id"]]

    job_skills = job_skills.dropna()
    job_skills = job_skills.drop_duplicates()

    return  job_skills


job_skills = job_skills_bridge(df,jobs,skills)

print(job_skills.head())
