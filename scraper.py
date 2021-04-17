#
# CSCI181 Final Project: 
# Names: Gabe, Samuel So
# 

import pandas as pd
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

POMONA_GEs_URL = (
    "https://tableau.campus.pomona.edu/views/GEdashboardforweb/DashboardforWeb?"
    ":embed=y&:display_count=n&:origin=viz_share_link&:showVizHome=n"
)

def selenium_click_download(driver, wait):
    print("Downloading Course List.xlsx...")
    # click download
    download_path = '//*[@id="download-ToolbarButton"]'
    driver.find_element_by_xpath(download_path).click()

    print("Getting crosstabs...")
    # select the crosstab option (allows to download excel/csv)
    crosstab_path = '//*[@id="DownloadDialog-Dialog-Body-Id"]/div/fieldset/button[3]'
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, crosstab_path)
        )
    ).click()

    # pick the "Course List" spreadsheet
    course_list_path = (
        '//*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]'
        '/div/div[1]/div[2]/div/div/div[7]/div/div/div'    
    )
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, course_list_path)
        )
    ).click()

    # and finally download (excel)
    final_download = (
        '//*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[3]/'
        'button'
    )
    driver.find_element_by_xpath(final_download).click()

def download_tableau_courses(driver, wait):
    try:
        # click clear all
        print("Clearing filters...")
        clear_all_path = "//*[@id='tabZoneId17']/div/div/div"
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, clear_all_path)
            )
        ).click()

        # get all the dropdowns. we can't get just one because the ids are always changing
        print("Waiting for updated courses...")
        discipline_path = (
            "//*[starts-with(@id, 'tab-ui-id-') and "
            "@class='tabComboBoxName' and "
            "text()='(All)']"
        )

        # wait for there to be 3 '(All)' fields
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"({discipline_path})[2]")
            )
        )
        
    except Exception as e:
        print(e)
        print("An error occurred trying to filter the data.")

    # series of download clicks. if it fails, the exception will keep trying (2 more times)
    max_attempts = 3
    while max_attempts:
        try:
            selenium_click_download(driver, wait)
            print("Courses successfully downloaded.")
            break

        except StaleElementReferenceException as s:
            print(s)
            print("Download error occurred. Trying again...")
            max_attempts -= 1
            
    if not max_attempts:
        print("Too many attempts. Closing...")

if __name__ == "__main__":

    if not os.path.exists('Course List.xlsx'):
        # scrape GEs from Tableau. Done by physically downloading the excel spreadsheet of courses
        print("Scraping GEs...")

        # chrome options set the download destination to current directory
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : os.path.abspath('.')}
        chromeOptions.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(executable_path='./chromedriver', options=chromeOptions)

        # open driver and create explicit waiter object
        driver.get(POMONA_GEs_URL)
        wait = WebDriverWait(driver, 10)

        download_tableau_courses(driver, wait)

        print("Waiting for courses...", end="")
        while not os.path.exists('Course List.xlsx'):
            print(".", end="")
            time.sleep(1)
        print()
        
    a = pd.read_excel('Course List.xlsx')
    print(a.head())