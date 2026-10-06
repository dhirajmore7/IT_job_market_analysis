from scraper.naukri.naukri_link_scraper import naukri_link_scraper

from scraper.naukri.naukri_scraper_data import naukri_scraper_data

from pathlib import Path
import pandas as pd
from datetime import date
from etl.config import naukri_link_data,history_data,job_role


max_pages = "all"

def naukri_job_link_scraper():


    global max_pages

    # Create folder if it doesn't exist
    naukri_link_data.parent.mkdir(parents=True,  exist_ok=True )
    

    print("Starting Naukri extraction...")

    df = pd.read_csv(naukri_link_data)

    print(df.head(5))


    # start scraping of link from  where last link was extracted
    if not df.empty:
        
        
        print("start scraping from  ",df['search_url'].iloc[len(df) - 1])
        
        last_url= df['search_url'].iloc[len(df) - 1]
        
        start_page = last_url.split('-')
        start_page =int(start_page[-1]) + 1
        
        if type(max_pages) == int:
            max_pages = (max_pages + start_page) 

    else:
        start_page = 0

    link_count = naukri_link_scraper(max_pages,job_role,start_page)

    print(f"Extracted rows: {link_count}")

    
    

    
    


    # scrap history 
    
    if naukri_link_data.exists():

        df_2 =pd.read_csv(naukri_link_data)
    

    scraping_history = [{"source":"Naukri.com","scrap_date":"","new_job_links":"","total_scraped_link":""}]

    df_1= pd.DataFrame(scraping_history)

    df_1['scrap_date']= date.today()
    df_1['new_job_links'] = link_count
    df_1['total_scraped_link']= len(df_2)

    # save history data in csv
    header2 = not history_data.exists()
    

    df_1.to_csv(history_data,mode='a',header=header2,index=False)

    print("\n")
    print(df_1)
    print('histroy data SAVED !')

    print(f"Saved {len(df)} rows to {naukri_link_data}")

    naukri_raw_data()


output_csv = Path("data/extracted_data/naukri_data/naukri_raw_jobs.csv")
def naukri_raw_data():

    naukri_scraper_data(naukri_link_data,output_csv)
    
    

if __name__ == "__main__":
    naukri_job_link_scraper()
    
    