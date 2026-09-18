import pandas as pd
from playwright.sync_api import sync_playwright

from pathlib import Path
naukri_job_link = Path("scraped_data/naukri.com_data/naukri_jobs_link.csv")

jobs = []

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        viewport={"width": 1280, "height": 900}
    )

    page = context.new_page()

    page.goto(
        "https://www.naukri.com/data-analyst-jobs",
        timeout=60000,
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(5000)

    print("Page title:", page.title())

    # Find job links
    job_links = page.locator(
        'a[href*="/job-listings-"]'
    )

    print("Job links found:", job_links.count())

    for i in range(job_links.count()):

        link = job_links.nth(i)

        title = link.inner_text().strip()
        url = link.get_attribute("href")

        if title and url:

            jobs.append({
                "job_title": title,
                "job_url": url
            })

            print(i, title)
            print(url)

    browser.close()


# Create DataFrame
df = pd.DataFrame(jobs)

# Remove duplicate URLs
df = df.drop_duplicates(
    subset=["job_url"]
)




# Save CSV
df.to_csv(
    naukri_job_link,
    index=False
)

print("\nFinal data:")
print(df)

print("\nSaved to naukri_jobs_link.csv")