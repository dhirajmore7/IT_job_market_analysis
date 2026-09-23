import pandas as pd
import re
from pathlib import Path
import string
from etl.config import skills

raw_data = Path("extracted_data/naukri_data/naukri_raw_jobs.csv")

clean_data = Path("processed_data/naukri/naukri_clean_data.csv")

city_state_csv = Path("extracted_data/naukri_data/india_city_state_mapping.csv")






def city_state_clean(df,city_state):

    # extract city from location
    df["city"] = (df["raw_location"].str.replace(r"\([^)]*\)", "", regex=True).str.replace(r",.*", "", regex=True).str.strip())

    # find state using city columns 

    temp_city_state = pd.read_csv(city_state_csv)
    city_zip = dict(zip(city_state['city'],city_state['state']),)

    df['state']=df['city'].map(city_zip)

    df['country']='India'


def add_missing_skills(row):

    # split key skills by , and store in variable 
    existing = str(row["key_skills"]).split(",")


    # remove extra spaces and empty string
    existing = [skill.strip() for skill in existing if skill.strip()]

    # convert to lower
    existing_lower = {skill.lower() for skill in existing}
    # convert description to lower 
    description = str(row["job_description"]).lower()

    for skill in skills:
        if skill.lower() in description:
            if skill.lower() not in existing_lower:
                existing.append(skill)
                existing_lower.add(skill.lower())

    return ", ".join(existing)








def main():

    # read csv raw data and city_state_csv
    df = pd.read_csv(raw_data)
    city_state = pd.read_csv(city_state_csv)

     # rename location column
    df = df.rename(columns={'location':'raw_location'})

    # created a new column order for new clean data csv

    new_order = ['job_title', 'company', 'raw_location', 'city', 'state', 'country','experience', 'min_salary','max_salary'
                'job_description', 'key_skills', 'posted_date','posted', 'rating', 'reviews',
                'job_url', 'scrape_date']

    df = df.reindex(columns=new_order)

     # find city and state
    city_state_clean(df,city_state)

     # add missing skills from description to key skills
    df["key_skills"] = df.apply(add_missing_skills, axis=1)





    print(df.columns)

    print(df.head())
    print(df['posted'])

main()

