import requests
from bs4 import BeautifulSoup
import os, time

PAGES = {   
"homepage":  "https://www.everettsd.org",
"calendar":  "https://www.everettsd.org/district-calendar",
"food_nutrition": "https://www.everettsd.org/food-nutrition-services",
"enrollment": "https://www.everettsd.org/general-enrollment",
"transportation": "https://www.everettsd.org/transportation",
"academics": "https://www.everettsd.org/academics",
"school_hours": "https://www.everettsd.org/about-us/schools-directory/district-and-school-hours",
"safety": "https://www.everettsd.org/safety-concern",

"employment": "https://www.everettsd.org/eps-employment",
"payments": "https://www.everettsd.org/payments",
"special_ed": "https://www.everettsd.org/special-education",
"counseling": "https://www.everettsd.org/counseling",
"athletics": "https://www.everettsd.org/athletics",
"summer_programs": "https://www.everettsd.org/summer-programs",
"health": "https://www.everettsd.org/health-services",
"parent_resources":"https://www.everettsd.org/parent-resources",
}

os.makedirs('data/raw', exist_ok=True)
    
def scrape_page(name, url):
    try:
        print(f'Scraping: {name}...')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['nav','footer','script','style','header']):
            tag.decompose()
        text = soup.get_text()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        clean = '\n'.join(lines)
        with open(f'data/raw/{name}.txt', 'w', encoding='utf-8') as f:
            f.write(f'SOURCE URL: {url}\n')
            f.write(f'PAGE NAME: {name}\n')
            f.write('='*50 + '\n')
            f.write(clean)
        print(f' Saved {len(clean)} characters')
        return True
    except Exception as e:
        print(f' ERROR: {e}')
        return False
    
success = 0
for name, url in PAGES.items():
    if scrape_page(name, url):
        success += 1
    time.sleep(1) # Be polite — wait 1 sec between requests
print(f'Done! {success}/{len(PAGES)} pages scraped')