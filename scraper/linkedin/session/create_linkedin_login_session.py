from playwright.sync_api import sync_playwright
from pathlib import Path

AUTH_FILE = Path("scraper/session/state.json")

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    # Replace with the login page of your permitted test site
    page.goto("https://linkedin.com/login")

    print("Log in manually in the browser.")
    input("After login is complete, press ENTER here...")

    # Save authenticated state
    context.storage_state(path=str(AUTH_FILE))

    print(f"Authentication state saved to {AUTH_FILE}")

    browser.close()