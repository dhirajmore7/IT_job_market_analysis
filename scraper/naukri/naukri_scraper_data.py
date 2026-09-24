import csv
import os
import time
import random
import pandas as pd
from datetime import date
from pathlib import Path
from playwright.sync_api import sync_playwright



# CONFIGURATION


# input_csv = Path("scraped_data/naukri.com_data/naukri_jobs_link.csv")

# output_csv = Path("scraped_data/naukri.com_data/naukri_jobs_raw.csv")


FIELDS = [ "scrap_job_title",
    "job_title",
    "company",
    "location",
    "experience",
    "salary",
    "job_description",
    "key_skills",
    "posted",
    "rating",
    "reviews",
    "job_url",
    "scrape_date"
]






# SAFE TEXT EXTRACTION


def get_text(page, selectors):

    for selector in selectors:

        try:

            locator = page.locator(selector).first

            if locator.count() > 0:

                text = locator.inner_text(timeout=3000).strip()

                if text:

                    return text

        except Exception:

            continue

    return ""


 
# JOB TITLE
 

def get_job_title(page):

    return get_text(page,
        [
            "h1.styles_jd-header-title__rZwM1",
            "h1.jd-header-title",
            "h1"
        ]
    )



# COMPANY


def get_company(page):

    return get_text(page,
        [
            "div.styles_jd-header-comp-name__MvqAI a",
            "a.styles_jd-header-comp-name__LAp7I",
            "a.comp-name",
            ".comp-name"
        ]
    )



# LOCATION


def get_location(page):

    return get_text(page,
        [
            "span.styles_jhc__location__W_pVs",
            "div.styles_jhc__location__W_pVs",
            ".location"
        ]
    )



# EXPERIENCE

def get_experience(page):

    return get_text(page,
        [
            "div.styles_jhc__exp__k_giM span",
            "div.styles_jhc__exp__k_giM"
        ]
    )



# SALARY


def get_salary(page):

    return get_text(page,
        [
            "div.styles_jhc__salary__jdfEC span",
            "div.styles_jhc__salary__jdfEC"
        ]
    )



# POSTED


def get_posted(page):

    try:

        stats = page.locator(
            "span.styles_jhc__stat__PgY67"
        )

        count = stats.count()

        for i in range(count):

            stat = stats.nth(i)

            label = stat.locator(
                "label"
            ).inner_text().strip()

            if label.startswith("Posted"):

                value = stat.locator(
                    "span"
                ).last.inner_text().strip()

                return value

    except Exception as e:

        print(
            f"Posted extraction error: {e}"
        )

    return ""


  
# OPENINGS
   

def get_openings(page):

    try:

        stats = page.locator(
            "span.styles_jhc__stat__PgY67"
        )

        for i in range(stats.count()):

            stat = stats.nth(i)

            label = stat.locator(
                "label"
            ).inner_text().strip()

            if label.startswith("Openings"):

                return stat.locator(
                    "span"
                ).last.inner_text().strip()

    except Exception:

        pass

    return ""


    
# APPLICANTS
     

def get_applicants(page):

    try:

        stats = page.locator(
            "span.styles_jhc__stat__PgY67"
        )

        for i in range(stats.count()):

            stat = stats.nth(i)

            label = stat.locator(
                "label"
            ).inner_text().strip()

            if label.startswith("Applicants"):

                return stat.locator(
                    "span"
                ).last.inner_text().strip()

    except Exception:

        pass

    return ""


      
# JOB DESCRIPTION
      

def get_job_description(page):

    selectors = [
        "div.styles_JDC__dang-inner-html__h0K4t",
        "div.styles_job-desc-container__txpyr",
        "div.job-desc",
        "section.job-desc"
    ]

    for selector in selectors:

        try:

            locator = page.locator(
                selector
            ).first

            if locator.count() > 0:

                text = locator.inner_text(
                    timeout=5000
                ).strip()

                if text:

                    return text

        except Exception:

            continue

    return ""


       
# KEY SKILLS
        

def get_key_skills(page):

    selectors = [
        "div.styles_key-skill__GIPn_ a",
        "div.styles_key-skill__GIPn_ span",
        ".styles_key-skill__GIPn_ a",
        ".styles_key-skill__GIPn_ span",
        ".key-skill a",
        ".key-skill span"
    ]

    skills = []

    for selector in selectors:

        try:

            elements = page.locator(
                selector
            )

            count = elements.count()

            for i in range(count):

                text = elements.nth(
                    i
                ).inner_text().strip()

                if text and text not in skills:

                    skills.append(text)

            if skills:

                break

        except Exception:

            continue

    return ", ".join(skills)


         
# RATING + REVIEWS
          

def get_rating_reviews(page):

    rating = ""
    reviews = ""

    try:

        rating = page.locator(
            "span.styles_amb-rating__4UyFL"
        ).first.inner_text(
            timeout=3000
        ).strip()

    except Exception:

        pass


    try:

        reviews = page.locator(
            "span.styles_amb-reviews__0J1e3"
        ).first.inner_text(
            timeout=3000
        ).strip()

    except Exception:

        pass


    return rating, reviews


# SCRAPE ONE JOB
                 

def scrape_job(page, job_url,df):

    

    data = {field: "" for field in FIELDS }


    # Always save URL

    data["job_url"] = job_url


    try:

        print("\n")
        print("=" * 90)

        print(f"Opening job URL:\n{job_url}")

        print("=" * 90)


                                
        # OPEN PAGE
                                

        page.goto(
            job_url,
            wait_until="domcontentloaded",
            timeout=30000
        )


        # Wait for page to settle
        time.sleep(
            random.uniform(2, 4)
        )

        # scrap_job_title

        job_row = df[df["job_url"] == job_url]

        if not job_row.empty:
            data["scrap_job_title"] = job_row.iloc[0]["job_title"]
        else:
            data["scrap_job_title"] = ""
                                
        # JOB TITLE
                                

        data["job_title"] = get_job_title(page)


                                
        # COMPANY
                                

        data["company"] = get_company(page)


                                
        # LOCATION
                                

        data["location"] = get_location(page)


                                
        # EXPERIENCE
                                

        data["experience"] = get_experience(page)


                                
        # SALARY
                                

        data["salary"] = get_salary(page)


                                
        # POSTED
                                

        data["posted"] = get_posted( page )


                                
        # JOB DESCRIPTION
                                

        data["job_description"] = get_job_description( page)


                                
        # KEY SKILLS
                                

        data["key_skills"] = get_key_skills(page)


                                
        # RATING + REVIEWS
                                

        (data["rating"],
        data["reviews"]) = get_rating_reviews( page)

        # SCRAPING DATE

        data["scrape_date"] = date.today()


                                
        

        
        # PRINT SCRAPED DATA
        
        print("\nSCRAPED DATA")
        print("-" * 50)

        print(
            "Job Title      :",
            data["job_title"]
        )

        print(
            "Company        :",
            data["company"]
        )

        print(
            "Location       :",
            data["location"]
        )

        print(
            "Experience     :",
            data["experience"]
        )

        print(
            "Salary         :",
            data["salary"]
        )

        print(
            "Posted         :",
            data["posted"]
        )

        print(
            "Key Skills     :",
            data["key_skills"]
        )

        

        print(
            "Rating         :",
            data["rating"]
        )

        print(
            "Reviews        :",
            data["reviews"]
        )

        print(
            "Description    :",
            len(data["job_description"]),
            "characters"
        )

        print("-" * 50)


        return data


    except Exception as e:

        print(
            f"ERROR scraping:\n{job_url}"
        )

        print(
            f"Error: {e}"
        )

        return data


                  
# SAVE DATA TO CSV 
                   

def save_to_csv(data,output_csv):

    file_exists = output_csv.exists()


    with open(
        output_csv,
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )


        # Write header only for new file
        if not file_exists:

            writer.writeheader()


        writer.writerow(
            data
        )


                     
# READ JOB URLS
                      

def get_job_urls(input_csv):

    print(
        f"\nReading input file:\n{input_csv}"
    )

    if not input_csv.exists():

        raise FileNotFoundError(
            f"Input CSV not found: {input_csv}"
        )


    df = pd.read_csv( input_csv )


    print(
        "CSV columns:",
        list(df.columns)
    )


                                            

    url_column = "job_url"

                                 
    # Clean URLs
                                                    

    urls = (
        df[url_column]
        .dropna()
        .astype(str)
        .str.strip()
    )


    urls = urls[
        urls != ""
    ]


    # Remove duplicates
    urls = urls.unique().tolist()


    return urls


                        
# GET ALREADY SCRAPED URLs
                        

def get_scraped_urls(output_csv):

    scraped_urls = set()


    if not output_csv.exists():

        return scraped_urls


    try:

        df = pd.read_csv(
            output_csv
        )


        if "job_url" in df.columns:

            scraped_urls = set(
                df["job_url"]
                .dropna()
                .astype(str)
                .str.strip()
            )


    except Exception as e:

        print(
            f"Could not read existing output: {e}"
        )


    return scraped_urls


                        
# MAIN
                        

def naukri_scraper_data(input_csv,output_csv):

    df = pd.read_csv(input_csv)                                               


    # GET URLS
                                                    

    urls = get_job_urls(input_csv)


    print( 
        f"\nTotal unique job URLs: {len(urls)}"
    )


                                                    
    # GET PREVIOUSLY SCRAPED URLS
                                                    

    scraped_urls = get_scraped_urls(output_csv)


    print(
        f"Already scraped: {len(scraped_urls)}"
    )


    remaining = [
        url
        for url in urls
        if url not in scraped_urls
    ]


    print(
        f"Remaining jobs: {len(remaining)}"
    )


    if not remaining:

        print(
            "\nAll jobs have already been scraped."
        )

        return


    
    # PLAYWRIGHT
    
    with sync_playwright() as p:

        print(
            "\nStarting Chromium..."
        )


        browser = p.chromium.launch(
            headless=False
        )


        context = browser.new_context(
            viewport={
                "width": 1366,
                "height": 768
            }
        )


        page = context.new_page()


                                
        # SCRAPE EACH JOB
                                

        for index, job_url in enumerate(
            remaining,
            start=1
        ):

            print(
                f"\nJOB {index}/{len(remaining)}"
            )


            try:

                data = scrape_job(page, job_url,df)

                
                # Save immediately
                
                save_to_csv( data,output_csv)


                scraped_urls.add( job_url  )


                print(
                    "\n✓ Saved to CSV"
                )


            except Exception as e:

                print(
                    f"\n✗ Failed: {e}"
                )


            #                                                                                  
            # Random delay
            #             

            delay = random.uniform(
                3,
                6
            )


            print(
                f"Waiting {delay:.1f} seconds..."
            )


            time.sleep(
                delay
            )


                                
        # CLOSE
                                

        browser.close()


    print("\n")
    print("=" * 90)

    print(
        "SCRAPING COMPLETED"
    )

    print(
        f"Output file: {output_csv}"
    )

    print("=" * 90)


                        
