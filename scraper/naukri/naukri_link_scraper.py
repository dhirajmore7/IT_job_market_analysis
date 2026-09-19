import pandas as pd
from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import random



# CONFIGURATION


naukri_job_link = Path( "scraped_data/naukri.com_data/naukri_jobs_link.csv")
                                         

BASE_URL = "https://www.naukri.com/data-analyst-jobs"

# Number of pages to scrape
MAX_PAGES = 2




# STORE JOBS


jobs = []





with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
        

    context = browser.new_context(viewport={ "width": 1280,"height": 900 })
        

    page = context.new_page()


    
    # LOOP THROUGH PAGES
    
    for page_number in range(1, MAX_PAGES + 1):

        
        print("=" * 80)
        print(f"SCRAPING PAGE {page_number}")
        print("=" * 80)


        
        # CREATE PAGE URL
        

        if page_number == 1:

            url = BASE_URL

        else:

            url = f"{BASE_URL}-{page_number}"


        print("Opening:", url)
                        
                   
            


        
        # OPEN PAGE
        

        try:

            page.goto(
                url,
                timeout=60000,
                wait_until="domcontentloaded"
            )

        except Exception as e:

            print(f"Page loading error: {e}")

            continue


        
        # WAIT FOR PAGE
        

        page.wait_for_timeout(5000)


        print("Page title:",page.title())


        
        # FIND JOB LINKS
        

        job_links = page.locator(
            'a[href*="/job-listings-"]'
        )


        count = job_links.count()


        print(
            f"Job links found on page {page_number}: {count}"
        )


        
        # IF NO JOBS FOUND
        

        if count == 0:

            print(
                f"No jobs found on page {page_number}."
            )

            print(
                "Stopping pagination."
            )

            break


        
        # EXTRACT JOB LINKS
        
        page_jobs = 0


        for i in range(count):

            try:

                link = job_links.nth(i)


                
                # GET TITLE
                

                title = link.inner_text().strip()


                
                # GET URL
                

                url = link.get_attribute(
                    "href"
                )


                
                # VALIDATE
                

                if title and url:

                    jobs.append(
                        {
                            "job_title": title,
                            "job_url": url
                        }
                    )


                    page_jobs += 1


                    print(
                        f"{i + 1}. {title}"
                    )

                    print(
                        f"   {url}"
                    )


            except Exception as e:

                print(
                    f"Error extracting job {i}: {e}"
                )


        print(
            f"\nJobs collected from page {page_number}: {page_jobs}"
        )


        
        # WAIT BEFORE NEXT PAGE
        

        if page_number < MAX_PAGES:

            delay = random.uniform(
                3,
                5
            )

            print(
                f"Waiting {delay:.1f} seconds before next page..."
            )

            time.sleep(
                delay
            )


    
    # CLOSE BROWSER
    

    browser.close()



# CREATE DATAFRAME


df = pd.DataFrame(
    jobs
)



# REMOVE DUPLICATE URLs


if not df.empty:

    df = df.drop_duplicates(
        subset=["job_url"]
    )



# RESET INDEX


df = df.reset_index(
    drop=True
)



# SAVE CSV


df.to_csv(
    naukri_job_link,
    index=False,
    encoding="utf-8-sig"
)



# FINAL RESULT


print("\n")
print("=" * 80)
print("SCRAPING COMPLETED")
print("=" * 80)


print(
    f"Total unique jobs: {len(df)}"
)


print(
    f"Saved to: {naukri_job_link}"
)


print("\nFinal data:")

print(
    df
)