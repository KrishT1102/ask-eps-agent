import requests
from bs4 import BeautifulSoup

#The page we want to fetch
url = "https://www.everettsd.org/district-calendar"

#Fetch the page
print("Fetching page...")
response = requests.get(url)

#Parse the HTML and extract text
soup = BeautifulSoup(response.text, 'html.parser')
text = soup.get_text()

#Clean up extra blank lines
lines = [line.strip() for line in text.splitlines() if line.strip()]
clean_text = '\n'.join(lines)

#Print first 2000 characters
print(clean_text[:2000])

#Save to a file
with open("calendar_page.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)

print("Done! Saved to calendar_page.txt")