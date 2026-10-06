import pandas as pd
import hashlib

from sqlalchemy import text
from etl.config import engine, clean_data_path


# Read cleaned data
df = pd.read_csv(clean_data_path)

print("Cleaned data loaded successfully")
print(df.head())


def company_table(df):

    # make all company nake title format 
    df["company"] = df["company"].str.strip().str.title()
    # drop duplicate and null values
    company = df[['company']].drop_duplicates()
    new_company = company.dropna()

    # compare new data with old data 
    previous_company = pd.read_sql(text("select company from companies"),con=engine)
    if not previous_company.empty:
        new_company = company[~company['company'].isin(previous_company['company'])]
            
    
    
    
    new_company = new_company.dropna()
    

    return new_company


def location_table(df):

    locations = df[['city','state','country']]

    locations = locations.drop_duplicates().dropna()

     #compare to previous location data so do not occur duplicate data
    pr_locations = pd.read_sql(text("select city,state,country from locations"),con=engine)

    new_locations = locations.merge(pr_locations[['city','state','country']],on=['city','state','country'],how='left',indicator=True)

    new_locations = new_locations[new_locations['_merge']=='left_only'].drop(columns="_merge")

    # new_locations.to_sql("locations",if_exists="append",index=False,con=conn)

    

    return new_locations


def jobs_table(df):
     # merge location table to get location_id
    location = pd.read_sql(text("select * from locations"),con=engine)

    if not location.empty:
        df = df.merge(location,on=['city','state','country'],how="left")

    # merge company table to get company_id
    company = pd.read_sql(text("select * from companies"),con=engine)

    if not company.empty:
        df = df.merge(company,on='company',how='left')
    

    
    jobs = df[[
                "job_title",
                "company_id",
                "location_id",
                "min_experience",
                "max_experience",
                "min_salary",
                "max_salary",
                "job_description",
                "posted_date",
                "job_url",
    
            ]].copy()
    
           
    jobs["job_url_hash"] = jobs["job_url"].apply( lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest() if pd.notna(x)  else None)
    
            # company = pd.read_sql(text("select * from companies"),con=conn)
    
            # jobs = jobs.merge(company,on=['city','state','country'],how="left")
    
    # compare new data with previour jobs data
    pr_jobs_data = pd.read_sql(text("select job_url from jobs"),con=engine)
    
    if not pr_jobs_data.empty :
        jobs = jobs[~jobs["job_url"].isin(pr_jobs_data["job_url"])]
    
    # jobs.to_sql("jobs",if_exists="append",con=conn,index=False)
    jobs["posted_date"] = pd.to_datetime(jobs["posted_date"],errors="coerce")

    jobs = jobs.dropna()

    return jobs
    
            
    
def skills_table(df):

    skills = df[["key_skills"]].copy()

    skills["skill_name"] = skills["key_skills"].str.split(",")

    skills = skills.explode("skill_name")

    skills["skill_name"] = ( skills["skill_name"].astype("string").str.strip().str.title())

    skills = skills.dropna(subset=["skill_name"])

    skills = skills[skills["skill_name"] != ""]

    skills = skills[["skill_name"]].drop_duplicates()

    pr_skills = pd.read_sql(text("select * from skills"),con=engine)

    if not pr_skills.empty:
        skills = skills[~skills['skill_name'].isin(pr_skills['skill_name'])]

    return skills


def job_skill_bridge(df):

    skills = df[['job_url','key_skills']]

    skills["skill_name"] = skills["key_skills"].str.split(",")
    
    skills = skills.explode("skill_name")
    
    skills["skill_name"] = ( skills["skill_name"].astype("string").str.strip().str.title())
    
    skills = skills.dropna(subset=["skill_name"])
    
    skills = skills[skills["skill_name"] != ""]
    
    skills = skills[["job_url","skill_name"]].drop_duplicates()

    

     # extract job_id from database table jobs
    jobs_id = pd.read_sql(text('select job_url,job_id from  jobs'),con=engine)
    print('job_id done')
    
    jobs_id = skills.merge(jobs_id,on='job_url',how='right')
    print('jobs join done')

    # extract skill_id from database table skills
    skill_id = pd.read_sql(text('select * from skills'),con=engine)

    jobs_skills = skill_id.merge(jobs_id,on='skill_name',how='left')

    job_skills = jobs_skills[['skill_id','job_id']]

    

    pr_jobs_skills = pd.read_sql(text('select * from job_skills'),con=engine)

    job_skills = job_skills[~job_skills['job_id'].isin(pr_jobs_skills['job_id'])]

    job_skills = job_skills.dropna()



    return job_skills


def company_rating_history_table(df):

    rating_history = df[['company','reviews','rating','posted_date']]

    # extract company data 
    company = pd.read_sql(text('select * from companies'),con=engine)

    rating_history = company.merge(rating_history,on='company',how='left')

    company_rating_history = rating_history[['company_id','rating','reviews','posted_date']].copy()

    company_rating_history['source']="Naukri"

    company_rating_history = company_rating_history.rename(columns={'posted_date':"collected_at"})
    company_rating_history["collected_at"] = pd.to_datetime(company_rating_history["collected_at"])
    company_rating_history = company_rating_history.dropna()


    new_data = pd.read_sql(text("select * from company_rating_history"),con=engine)

    new_data = new_data.merge(
        company_rating_history[["company_id", "collected_at"]],on=["company_id", "collected_at"],how="left",indicator=True )

    # Keep only records that don't already exist
    new_data = new_data[new_data["_merge"] == "left_only"]

    # Remove merge helper column
    new_data = new_data.drop(columns=["_merge"])

   

    return new_data
    

    

    
def load(df):

    company = company_table(df)
    
    location = location_table(df)
    
    jobs = jobs_table(df)
    
    skills = skills_table(df)
    
    job_skills = job_skill_bridge(df)
    
    company_rating_history = company_rating_history_table(df)

    print(jobs.dtypes)


    tables = {'companies':company,
              "locations":location,
              "jobs":jobs,
              "skills":skills,
              "job_skills":job_skills,
              "company_rating_history":company_rating_history}

    with engine.begin() as conn:
        try:
            for table_name , table in tables.items():
                if not table.empty:
                    print(len(table),"table length")
                
                    print('='*50)
                    print(table_name,"data ready to insert in database")
                    table.to_sql(table_name,if_exists='append',con=conn,index=False)
                    
                    print(table_name,":table sucessfully inserted")
                    print("=" * 50)

                else:
                    print(table_name,"New data not found data allready fill")

        except Exception as e:
            print('database error transaction failed',e)

load(df)










