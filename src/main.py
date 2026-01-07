"""
Rottentomatoes Data Scraper
- Steps:
    1. HTTP Request
    2. Header & Response Handling
    3. HTML Parsing
    4. Human engineering behavior Simulation
    5. Data Extraction
"""

from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import json
import random
from pathlib import Path
from datetime import datetime

# Target URL
URL = "https://www.rottentomatoes.com/browse/movies_in_theaters/"

# Selectors (from your selectors.md)
SEL_ITEMS = "div.flex-container"                    # All items selector
SEL_NAME = "span.p--small"                          # Name
SEL_TOMATOES = 'rt-text[slot="criticsScore"]'       # Tomatoes_scores
SEL_POPCORN = 'rt-text[slot="audienceScore"]'       # Popcorn
SEL_DATE = "span.smaller"                           # Date
SEL_LOAD_MORE = "div.discovery__actions > button"   # Load more


def accept_cookies_if_present(page) -> None:
    """
    Attempt to accept cookie/consent banners if they appear.
    Uses common consent selectors; safely does nothing if not present.
    """
    candidates = [
        "button#onetrust-accept-btn-handler",   # common OneTrust accept button
        "button:has-text('Accept')",
        "button:has-text('I Agree')",
    ]

    for sel in candidates:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=1500):
                btn.click()
                page.wait_for_timeout(800)  
                return
        except PlaywrightTimeoutError:
            pass


def safe_text(scoped_locator, css: str, timeout_ms: int = 1500) -> str:
    """
    Beginner-friendly helper:
    - Avoids Playwright strict-mode crashes by always taking `.first`
    - Returns empty string if element is missing / slow
    """
    try:
        loc = scoped_locator.locator(css).first
        return (loc.inner_text(timeout=timeout_ms) or "").strip()
    except PlaywrightTimeoutError:
        return ""


with Camoufox(
    headless=False,
    persistent_context=True,
    user_data_dir="user_data_dir",
    os=("windows",),
    i_know_what_im_doing=True,
) as browser:

    page = browser.new_page()

    # 1) HTTP Request
    page.goto(URL, wait_until="domcontentloaded")

    # Handle cookies/consent (if shown)
    accept_cookies_if_present(page)

    # 4) Human engineering behavior Simulation
    page.mouse.move(random.randint(0, 800), random.randint(0, 600))
    page.wait_for_timeout(random.randint(2000, 5000))  # human-ish pause

    # 2) Header & Response Handling (ensure the core XHR/JS content is in)
    # Note: "networkidle" can be unreliable on modern sites; we wait on a stable selector instead.
    page.wait_for_selector(SEL_ITEMS, timeout=30_000)

    # 3) HTML Parsing / JS-render confirmation (DOM manipulation)
    # Confirm items container is present before extracting.
    items = page.locator(SEL_ITEMS)

    # Optional: click "Load more" a few times (beginner-friendly approach)
    for _ in range(2):
        try:
            btn = page.locator(SEL_LOAD_MORE).first
            if btn.is_visible(timeout=2000):
                btn.scroll_into_view_if_needed()
                btn.click()
                page.wait_for_timeout(random.randint(800, 1500))  # let new items render
        except PlaywrightTimeoutError:
            break

    # 4) Human engineering behavior Simulation
    human_delay_ms = int(random.uniform(1000, 3000))  # milliseconds
    page.wait_for_timeout(human_delay_ms)

    # 5) Data Extraction
    movies_data = []
    for i in range(items.count()):
        movie = items.nth(i)

        data = {
            "Name": safe_text(movie, SEL_NAME),
            "Tomatoes_score": safe_text(movie, SEL_TOMATOES),
            "Popcorn_score": safe_text(movie, SEL_POPCORN),
            "Date": safe_text(movie, SEL_DATE),
        }
        movies_data.append(data)

    # Write JSON to file
    out_dir = Path(r"C:\Users\Mteto\Desktop\Practice\rottentomatoes\docs")
    out_dir.mkdir(exist_ok=True, parents=True)
    out_file = out_dir / f"rottentomatoes_movies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_file.write_text(json.dumps(movies_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved to: {out_file}")

    page.close()
