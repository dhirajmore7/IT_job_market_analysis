from scraper.naukri.naukri_link_scraper import naukri_link_scraper

from scraper.naukri.naukri_scraper_data import naukri_scraper_data

from pathlib import Path
import pandas as pd
from datetime import date


naukri_link_data = Path("extracted_data/naukri_data/naukri_link_data.csv")

# previous_data = Path("extracted_data/naukri_data/naukri_link_data.csv")

history_data = Path("extracted_data/naukri_data/naukri_scrap_history.csv")


def naukri_job_link_scraper():

    print("Starting Naukri extraction...")

    df = naukri_link_scraper()

    print(f"Extracted rows: {len(df)}")

    if df.empty:
        print("No data extracted.")
        return

    # Remove duplicate URLs

    df = df.drop_duplicates(subset=["job_url"])

    

    # Create folder if it doesn't exist
    naukri_link_data.parent.mkdir(parents=True,  exist_ok=True )

    # Don't repeat CSV header when appending
    header = not naukri_link_data.exists()

    #before data convert to csv compare it with previous  data
    previous_data = pd.read_csv(naukri_link_data)

    previous_url = set(previous_data['job_url'])

    df = df[~df['job_url'].isin(previous_url)]



    # data convert to csv

    df.to_csv(naukri_link_data,  mode="a",  header=header,  index=False  )


    # scrap history 
    df_2 =pd.read_csv(naukri_link_data)
    

    scraping_history = [{"source":"Naukri.com","scrap_date":"","new_job_links":"","total_scraped_link":""}]

    df_1= pd.DataFrame(scraping_history)

    df_1['scrap_date']= date.today()
    df_1['new_job_links'] = len(df)
    df_1['total_scraped_link']= len(df_2)

    # save history data in csv
    header2 = not history_data.exists()
    

    df_1.to_csv(history_data,mode='a',header=header2,index=False)

    print("\n")
    print(df_1)
    print('histroy data SAVED !')

    print(f"Saved {len(df)} rows to {naukri_link_data}")

    naukri_raw_data()


output_csv = Path("extracted_data/naukri_data/naukri_raw_jobs.csv")
def naukri_raw_data():
    naukri_scraper_data(naukri_link_data,output_csv)
    
    

if __name__ == "__main__":
    naukri_job_link_scraper()

