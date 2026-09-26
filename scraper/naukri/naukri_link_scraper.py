import pandas as pd
from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import random
from playwright.sync_api import Page
import re


# CONFIGURATION


naukri_link_data = Path( "extracted_data/naukri_data/naukri_link_data.csv")
                                         

# base_url = "https://www.naukri.com/data-analyst-jobs"





# STORE JOBS



jobs = []

def save_to_csv():

    global jobs

    df = pd.DataFrame(jobs)
    naukri_link_data.parent.mkdir(parents=True,  exist_ok=True )

    df = df.drop_duplicates()

    # before save to csv data compare to previous data
    if naukri_link_data.exists():
        previous_data = pd.read_csv(naukri_link_data)

        previous_data = set(previous_data['job_url'])

        df = df[~df['job_url'].isin(previous_data)]

    # do not repeat header
    header = not naukri_link_data.exists()

    # conver df to csv

    df.to_csv(naukri_link_data,mode='a',header=header,index=False)

    # empty jobs list after saving
    jobs = []


def extract_job_search_total(role,start_page=0):

    search_url = f"https://www.naukri.com/{role}-jobs-{start_page}"
    
    with sync_playwright() as p:
    
        browser = p.chromium.launch(headless=False)
    
        context =  browser.new_context(viewport={'width':1280,'height':900})       
            
        page = context.new_page()
    
        page.goto( search_url, timeout=70000, wait_until="domcontentloaded"   )
        
        print(page.title())

        page_title = page.title()

        

        if any(char.isdigit() for char in page_title):
            print(page_title)
            total_jobs = int(re.findall(r"\d+",page_title)[0])
            return total_jobs

        else:
        
            wrapper = page.locator('div[class*="h1-wrapper"]').first
            wrapper.wait_for(state="visible", timeout=10000)

            count_string = wrapper.locator('span[class*="count-string"]').first.inner_text().strip()
            title = wrapper.locator('h1[class*="h1-content"]').first.inner_text().strip()

            start = end = total = None
            m = re.match(r"(\d+)\s*-\s*(\d+)\s*of\s*(\d+)", count_string)
            if m:
                start, end, total = (int(g) for g in m.groups())

            # return {'message':'total jobs not found by page.title()',
            #         'count_string':count_string,
            #         'start':start,
            #         'end':end,
            #         'total':total}
            return total

def link_scraper(max_pages,role,page_number=0):

    
    
    base_url = f"https://www.naukri.com/{role}-jobs"


    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
            

        context = browser.new_context(viewport={ "width": 1280,"height": 900 })
            

        page = context.new_page()


        
        # LOOP THROUGH PAGES
        count_jobs_link = 0
        
        while page_number < max_pages :

            
            print("=" * 80)
            print(f"SCRAPING PAGE {page_number}")
            print("=" * 80)


            
            # CREATE PAGE URL
            

            if page_number == 1:

                search_url = base_url

            else:

                search_url = f"{base_url}-{page_number}"


            print("Opening:", search_url)
                            
                    
                


            
            # OPEN PAGE
            

            try:

                page.goto(
                    search_url,
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

                print( "Stopping pagination.")

                break


            
            # EXTRACT JOB LINKS
            
            page_jobs = 0


            for i in range(count):

                try:

                    link = job_links.nth(i)


                    
                    # GET TITLE
                    

                    title = role.replace('-'," ").title()


                    
                    # GET URL
                    

                    url = link.get_attribute(
                        "href"
                    )


                    
                    # VALIDATE
                    

                    if title and url and search_url:

                        jobs.append(
                            {   "search_url":search_url,
                                "job_title": title,
                                "job_url": url
                            }
                        )


                        page_jobs += 1


                        print( f"{i + 1}. {title}"   )

                        print( f"   {url}") 
                           
                    


                except Exception as e:

                    print(
                        f"Error extracting job {i}: {e}"
                    )


            print(
                f"\nJobs collected from page {page_number}: {page_jobs}"
            )


            
            # WAIT BEFORE NEXT PAGE
            

            if page_number < max_pages:

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

            page_number += 1

            count_jobs_link += len(jobs)


            save_to_csv()


        
        # CLOSE BROWSER
        

        browser.close()

    return count_jobs_link


def naukri_link_scraper(max_pages,role,start_page):

    # to find last_page for the give job role
    if max_pages.lower() == 'all':

        total_jobs = extract_job_search_total(role,start_page)

        print('total jobs:',total_jobs)

        max_pages = (total_jobs//20) + 1
        print('pages to scrap:',max_pages)
        
        print("scraping all pages:\n",max_pages,"\nfor job role:",role)
    

    # if start_page.empty():
    #     start_page = 0
    


    link_count=link_scraper(max_pages,role,start_page)


    
    



    

    print("\n")
    print("=" * 80)
    print("SCRAPING COMPLETED")
    print("=" * 80)


    print(
        f"Total unique jobs: {link_count}"
    )


    print(
        f"Saved to: {naukri_link_data}"
    )


    print("\nFinal data:")
    print(link_count)

    

    return link_count