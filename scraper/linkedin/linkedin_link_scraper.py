from playwright.sync_api import sync_playwright
from pathlib import Path


import time

import random

session_path=Path("scraper/linkedin/session/state.json")
data_path = Path("scraped_data/linkedin_data/linkedin_jobs_link.csv")

def scrape_page(page):
    jobs = []

    #  structured card selectors
    try:
        cards = page.locator(
            'li.jobs-search-results__list-item,'
            'div.job-card-container,'
            'div.job-card-list'
        )
        for i in range(cards.count()):
            try:
                card     = cards.nth(i)

                title_el = card.locator(
                    '.job-card-list__title,'
                    '.job-card-container__link,'
                    'a[data-control-name="job_card_title"]'
                ).first

                title    = title_el.inner_text().strip() if title_el.count() > 0 else ""

                link_el  = card.locator('a[href*="/jobs/view/"]').first

                href     = link_el.get_attribute("href") if link_el.count() > 0 else ""

                if href and not href.startswith("http"):
                    href = "https://www.linkedin.com" + href
                if href and "/jobs/view/" in href and title:
                    jobs.append({"title": title.split("\n")[0].strip(), "url": href.split("?")[0]})
            except Exception:
                pass
        if jobs:
            return jobs
    except Exception:
        pass

    #  fallback anchor scan
    for a in page.locator("a").all():
        try:
            href = a.get_attribute("href") or ""
            if not href.startswith("http"):
                href = "https://www.linkedin.com" + href
            if "/jobs/view/" not in href:
                continue
            title = a.inner_text().strip().split("\n")[0].strip()
            if title:
                jobs.append({"title": title, "url": href.split("?")[0]})
        except Exception:
            pass
    return jobs


def human_delay(lo=None, hi=None):
    time.sleep(random.uniform(lo or DELAY_MIN, hi or DELAY_MAX))
page_num = 0
max_page = 1
while page_num < max_page:
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            storage_state=session_path,
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()

        role = "Data Analyst"
        

        
        url = (
                        f"https://www.linkedin.com/jobs/search/"
                        f"?keywords={role.replace(' ', '%20')}"
                        f"&location=India&start={page_num * 25}"
                    )
        
        try:
            page.goto(url, timeout=60000)

            # print(page)
            human_delay(3, 5)
        except Exception as e:
            print(f"  Page load error: {e}")

        found = scrape_page(page)

        

            

            
        total_saved = len(found)
        print(f"  Page {page_num+1}: {len(found)} jobs  (total: {total_saved})")
        for i in found:
            print(i)



        all_jobs = {}

        previous_unique = 0

        for scroll_number in range(20):

            # -----------------------------------------
            # Scrape currently rendered jobs
            # -----------------------------------------

            current_jobs = scrape_page(page)

            for job in current_jobs:
                all_jobs[job["url"]] = job

            print(
                f"Scroll {scroll_number + 1}: "
                f"Visible = {len(current_jobs)}, "
                f"Unique = {len(all_jobs)}"
            )

            
            # Find the largest scrollable DIV
            

            panel_info = page.locator("div").evaluate_all("""
                elements => elements
                    .filter(e => {
                        const s = getComputedStyle(e);

                        return (
                            (s.overflowY === "auto" ||
                            s.overflowY === "scroll") &&
                            e.scrollHeight > e.clientHeight &&
                            e.clientHeight > 400
                        );
                    })
                    .map((e, index) => ({
                        index: index,
                        scrollHeight: e.scrollHeight,
                        clientHeight: e.clientHeight,
                        scrollTop: e.scrollTop
                    }))
                    .sort((a, b) => b.scrollHeight - a.scrollHeight)
            """)

            if not panel_info:
                print("No scrollable panel found.")
                break

            # print("Scrollable panels:", panel_info)

            
            # Scroll the largest panel
            

            result = page.locator("div").evaluate_all("""
                elements => {

                    const candidates = elements.filter(e => {

                        const s = getComputedStyle(e);

                        return (
                            (s.overflowY === "auto" ||
                            s.overflowY === "scroll") &&
                            e.scrollHeight > e.clientHeight &&
                            e.clientHeight > 400
                        );

                    });

                    if (candidates.length === 0) {
                        return null;
                    }

                    candidates.sort(
                        (a, b) => b.scrollHeight - a.scrollHeight
                    );

                    const element = candidates[0];

                    const oldTop = element.scrollTop;

                    element.scrollTop += element.clientHeight;

                    return {
                        oldTop: oldTop,
                        newTop: element.scrollTop,
                        scrollHeight: element.scrollHeight,
                        clientHeight: element.clientHeight
                    };
                }
            """)

            # print("Scroll result:", result)

            if result is None:
                break

            if result["newTop"] == result["oldTop"]:
                print("Reached bottom.")
                break
            
            # Wait for new jobs

            page.wait_for_timeout(2000)

            
            # Check whether new jobs appeared
            

            if len(all_jobs) == previous_unique:

                print("No new jobs found.")

                # Don't immediately stop because the DOM
                # may need another scroll/render cycle.
                # Try one more cycle.

            previous_unique = len(all_jobs)
        
        
        jobs = list(all_jobs.values())

        for i in jobs:
            print(i)

        print()
        print("=" * 60)
        print("FINAL RESULT")
        print("=" * 60)

        print("Total unique jobs:", len(jobs))

        import pandas as pd

        df = pd.DataFrame(all_jobs.values())

        df.to_csv(data_path,mode='a',header=False, index=False)
        page_num += 1

       

    