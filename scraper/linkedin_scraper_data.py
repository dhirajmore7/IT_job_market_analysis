import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import date

from pathlib import Path
jobs_data = Path("scraped_data/linkedin_data/linkedin_jobs_raw_data.csv")

jobs_link=Path("scraped_data/linkedin_data/linkedin_jobs_link.csv")

session = Path("scraper/session/state.json")

df = pd.read_csv(jobs_link)

print(df)

jobs = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state=session
    )
    a = 1
    for url in df["url"].head(10):

        print("Opening:", url)

        detail_page = context.new_page()

        #  Open the job URL
        detail_page.goto(
            url,
            wait_until="domcontentloaded"
        )

        #  time to render
        detail_page.wait_for_timeout(3000)

        title = detail_page.title() 

        print("Page title:", detail_page.title())

        # Get the company name and URL
        company_locator = detail_page.locator(
            'a[href*="/company/"]'
                )

        company = ""
        company_url = ""
        

        if company_locator.count() > 0:

            company = company_locator.first.inner_text().strip()

            company_url = company_locator.first.get_attribute("href")

        print(a,"Company:", company)
        print(a,"Company URL:", company_url)

        # work place

        metadata_links = detail_page.locator(
            'a[href*="/jobs/view/"]'
        )

        print(a,"Found:", metadata_links.count())

        for i in range(metadata_links.count()):
            print(
                i,
                metadata_links.nth(i).inner_text()
            )
        workplace_type = metadata_links.nth(0).inner_text().strip()
        employment_type = metadata_links.nth(1).inner_text().strip()


       

        description_locator = detail_page.locator(
            '[data-testid="expandable-text-box"]'
        )

        if description_locator.count() > 0:
            description = description_locator.first.inner_text()
        else:
            description = ""


        # location,posted , aplicants
# Wait for the metadata paragraph to appear.
                # Instead of hardcoding the messy class list, target it more robustly:
                # a <p> whose direct children are multiple <span> tags separated by "·"
        selector = "p:has(span):has-text('ago')"  # adjust if needed
        detail_page.wait_for_selector(selector, timeout=15000)
    
        element = detail_page.query_selector(selector)
    
                # Get all span texts inside that <p>, cleaned up
        spans = element.query_selector_all("span")
        texts = [s.inner_text().strip() for s in spans if s.inner_text().strip() and s.inner_text().strip() != "·"]
    
                # texts now looks like:
                # ["Ajmer, Rajasthan, India", "1 month ago", "Over 100 people clicked apply"]
        data = {
                    "location": texts[0] if len(texts) > 0 else None,
                    "posted": texts[1] if len(texts) > 1 else None,
                    "applicants": texts[2] if len(texts) > 2 else None,
                }

        location = texts[0] if len(texts) > 0 else None
        posted = texts[1] if len(texts) > 1 else None

        applicants = texts[2] if len(texts) > 2 else None


            

        

       
        detail_page.close()

        job_data = {
            "url": url, 
            "title": title,
            "company": company,
            "company_url": company_url,
            "workplace_type": workplace_type,
            "employment_type": employment_type,
            "location":location,
            "posted":posted,
            "applicants":applicants,
            "description": description,
            "scrap_date" :date.today()
        }
        jobs.append(job_data)

        # df = pd.DataFrame(jobs)

        # df.to_csv("jobs_raw.csv",mode='a' ,index=False)

        # print(df)
    

    browser.close()

df = pd.DataFrame(jobs)

df.to_csv(jobs_data,mode='a' ,index=False)

print(df)