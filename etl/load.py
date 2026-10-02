import pandas as pd

from pathlib import Path
import hashlib
from etl.config import engine



# Read cleaned data

file_path = Path("processed_data/naukri/naukri_clean_data.csv")
df = pd.read_csv(file_path)

print("Data loaded successfully")
print(df.head())



# 1. COMPANY TABLE
def comapany_table(df):
    company = df[["company"]].drop_duplicates().copy()

    company = company.reset_index(drop=True)
    # company.insert(0, "company_id", range(101, 101 + len(company)))

    

    company.dropna(inplace=True)
    
    return company



# location table
def location_table(df):

    location = df[["city","state","country"]].drop_duplicates().copy()

    location = location.dropna()

    # add location id column in loacation data
    # location.insert(0, "location_id", range(1, len(location) + 1))

    

    return location



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

    # skills.insert(0, "skill_id", range(1, len(skills) + 1))

    skills = skills.rename(columns={"key_skills": "skill_name"})

    
    return skills

# generate hash
def generate_url_hash(url):

    if pd.isna(url):
        return None

    url = str(url).strip()

    return hashlib.sha256(
        url.encode("utf-8")
    ).hexdigest()


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

    # add sha in table for job url
    df['job_url_hash'] = df['job_url'].apply(generate_url_hash)

    # Add company ID
    jobs = jobs.merge(company, on="company", how="left")

    # Add location ID
    jobs = jobs.merge(location, on=['city','state','country'], how="left")
    
    jobs = jobs[
        [
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



# job_skills table bridge

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




# company_rating_history table

def company_rating_history(df,company):
    rating_history = df[ ["company", "rating", "reviews","posted_date"]].drop_duplicates().copy()

    rating_history = rating_history.merge(
        company,
        on="company",
        how="inner"
    )

    rating_history.rename(columns={'posted_date':"collected_at"},inplace=True)

    rating_history = rating_history[
        ["company_id", "rating", "reviews","collected_at"]
    ]

    rating_history["source"] = "Naukri"
    

    print("Company rating history")
    print(rating_history.head())

    return rating_history






def load_main():

    company=comapany_table(df)
    location = location_table(df)
    jobs = jobs_table(df,company,location)
    skills = skills_table(df)
    job_skill = job_skills_bridge(df,jobs,skills)
    rating_history = company_rating_history(df,company)


    tables={'company':company,
            'location':location,
            'jobs':jobs,
            'job_skill':job_skill,
            'company_rating_history':rating_history}

    
    try:

        with engine.begin() as conn:

            for table_name , table in tables.items():
                print('='*50)
                print(table_name,"Table loading to database\n")

                table.to_sql(table_name,con=conn,if_exists='append',index=False)

                print(table_name,": data sucessfully inserted in database ")
                print('='*50)

        print('all table  load sucessfuly. Transaction complete')

    except Exception as e:
        print('etl loading failed:',e)

load_main()