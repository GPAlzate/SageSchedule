#
# CSCI181 Final Project: 
# Names: Gabe, Samuel So
# 

from bs4 import BeautifulSoup
import requests
import re

print("Scraping...")

# webpage to scrape majors from
ROOT_URL = 'https://catalog.pomona.edu/' 
MAJORS_URL = f'{ROOT_URL}content.php?catoid=37&navoid=7542'
response = requests.get(url=MAJORS_URL, verify=False)
majors_page = response.text

# soup scraper object
soup = BeautifulSoup(majors_page, 'html.parser')

# all the majors begin with 'preview_entity'
MAJOR_PAGES = soup.find_all('a', href=re.compile("^preview_entity"))

# build a mapping from each major's name to their major page
MAJOR_DICT = {}
for page in MAJOR_PAGES:
    major_name = re.sub(r"Go to information for (.*)\.", r"\1", page.get_text())
    major_url = f"{ROOT_URL}{page.get('href')}"
    MAJOR_DICT[major_name] = major_url