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
import json
import random
import time
from pathlib import Path
from datetime import datetime

with Camoufox(
    headless=True,
    persistent_context=True,
    user_data_dir="user_data_dir",
    os=("windows",),
    i_know_what_im_doing=True,
    ) as browser:
    
    page = browser.new_page()
    # HTTP Request
    page.goto("https://www.rottentomatoes.com/browse/in-theaters/")
    
    # Simulate human behavior
    page.mouse.move(random.randint(0, 800), random.randint(0, 600))
    page.wait_for_timeout(random.randint(2000, 5000))   # captha delay simulation
    
    # header & response handling (ensure XHR/fetch completed)
    page.wait_for_load_state("networkidle", timeout=30000)
    
    # HTML Parsing / JS-render confirmation (DOM manipulation)
    page.wait_for_selector("div.flex-container", timeout=30000)
    
    # Human engineering behavior Simulation
    human_delay = random.uniform(1., 3.0)
    page.wait_for_timeout(human_delay)
    
    # Data Extraction
    movies = page.locator('div.flex-container')
    
    movies_data = []
    
    for movie in movies.all():
        data = {
            'Name': movie.locator('span.p--small').inner_text(),
            'Tomatoes_score': movie.locator('rt-text[slot="criticsScore"]').inner_text(),
            'Popcorn_score': movie.locator('rt-text[slot="audienceScore"]').inner_text(),
            'Date': movie.locator('span.smaller').inner_text(),
        }
        movie_data.append(data)
        
    # Write JSON to file
    out_dir = Path(r"C:\Users\Mteto\Desktop\Practice\rottentomatoes")
    out_dir.mkdir(exist_ok=True, parents=True)
    out_file = out_dir / f"rottentomatoes_movies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_file.write_text(json.dumps(movies_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"ĐY'ó Saved to: {out_file}")

    page.close()