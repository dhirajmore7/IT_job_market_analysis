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






def get_posted_date(row):

    scrape_date = pd.to_datetime(row["scrape_date"]).normalize()
    posted = row["posted"]

    if pd.isna(posted):
        return pd.NaT

    posted = str(posted).strip().lower()

    # Today
    if posted == "today":
        return scrape_date

    # 3+ weeks ago
    if "3+" in posted and "week" in posted:
        return scrape_date - pd.Timedelta(weeks=3)

    # 1 week ago, 2 weeks ago, 3 weeks ago
    if "week" in posted:
        weeks = int(posted.split()[0])
        return scrape_date - pd.Timedelta(weeks=weeks)

    # 1 day ago, 2 days ago, 3 days ago
    if "day" in posted:
        days = int(posted.split()[0])
        return scrape_date - pd.Timedelta(days=days)

    return pd.NaT




def main():

    # read csv raw data and city_state_csv
    df = pd.read_csv(raw_data)
    city_state = pd.read_csv(city_state_csv)

     # rename location column
    df = df.rename(columns={'location':'raw_location'})

    # created a new column order for new clean data csv

    new_order = ['job_title', 'company', 'raw_location', 'city', 'state', 'country','experience', 'min_salary','max_salary',
                'job_description', 'key_skills', 'posted_date','posted', 'rating', 'reviews',
                'job_url', 'scrape_date']

    df = df.reindex(columns=new_order)

     # find city and state
    city_state_clean(df,city_state)
    print('city_state done')
    
     # add missing skills from description to key skills
    df["key_skills"] = df.apply(add_missing_skills, axis=1)

    # find posted date from posted
    df["posted_date"] = df.apply(get_posted_date, axis=1)


    print(df[['posted','posted_date']])



   

main()

