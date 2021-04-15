#
# CSCI181 Final Project: 
# Names: Gabe, Samuel So
# 


from bs4 import BeautifulSoup
from tableauscraper import TableauScraper as ts
import requests
import re

print("Scraping...")

# # webpage to scrape majors from
# ROOT_URL = 'https://catalog.pomona.edu/' 
# MAJORS_URL = f'{ROOT_URL}content.php?catoid=37&navoid=7542'
# response = requests.get(url=MAJORS_URL, verify=False)
# majors_page = response.text

# # soup scraper object
# soup = BeautifulSoup(majors_page, 'html.parser')

# # all the majors begin with 'preview_entity'
# MAJOR_PAGES = soup.find_all('a', href=re.compile("^preview_entity"))

# # build a mapping from each major's name to their major page
# MAJOR_DICT = {}
# for page in MAJOR_PAGES:
#     major_name = re.sub(r"Go to information for (.*)\.", r"\1", page.get_text())
#     major_url = f"{ROOT_URL}{page.get('href')}"
#     MAJOR_DICT[major_name] = major_url

# Tableau link contains courses with their gen ed requirements (Area and Overlays)
POMONA_TABLEAU_URL = (
    "https://tableau.campus.pomona.edu/views/GEdashboardforweb/DashboardforWeb"
) 
print(POMONA_TABLEAU_URL)
ts = ts()
ts.loads(POMONA_TABLEAU_URL)

# courses in dataframe. each course has 5 rows (1 per requirement to fulfill)
courses = ts.getWorksheet("Course List")

# list of all possible discipline filters
disciplines = courses.getFilters()[2]['values']

# iterate through each subjects and scrape the subjects one filter at a time
for subj in disciplines:

    # get the courses only for that subject
    wb = courses.setFilter('Disciplines', subj)
    filtered_ws = wb.getWorksheet('Course List')   