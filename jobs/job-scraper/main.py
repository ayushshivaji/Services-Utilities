from selenium import webdriver
import argparse
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


'''

browser = webdriver.Chrome()
browser.get("https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite")

search_bar = browser.find_element(By.CSS_SELECTOR, "input[placeholder*='Search for jobs or keywords']")
search_bar.send_keys("devops")
search_bar.send_keys(Keys.RETURN)
raw_jobs_array = []


soup = BeautifulSoup(browser.page_source, 'html.parser')
a = soup.select("a[href*='NVIDIAExternalCareerSite/job/']")
raw_jobs_array.extend(a)
next_button = browser.find_element(By.CSS_SELECTOR, "button[data-uxi-element-id='next']")

job_list = []
for job_element in raw_jobs_array:
    job_list.append("https://nvidia.wd5.myworkdayjobs.com" + job_element.get('href'))


time_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data = {
            "Jobs": job_list,
            "Date Added": [time_added]*len(job_list),
            "Applied": [False]*len(job_list)
        }


df = pd.DataFrame(data)

'''
search_keywords = ["Devops", "SRE", "Site Reliability"]

class JobScraper:
    def __init__(self, headless):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")  # Optional, improves headless stability
            options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome(options=options)

    def locate_and_search(self ,locate_search_box_by, search_box_locator, keyword):
        # print("search_box_locator", search_box_locator, "locate_search_box_by", locate_search_box_by) # TODO : testing
        locator_strategy = getattr(By, locate_search_box_by.split(".")[1])
        # time.sleep(50) # testing
        wait = WebDriverWait(self.browser, 100)
        search_bar = wait.until(
            EC.presence_of_element_located((locator_strategy, search_box_locator))  # Replace with actual ID or locator
        )
        # search_bar = self.browser.find_element(locator_strategy, search_box_locator)
        print("Page loaded")
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)

    def search_website_for_jobs(
            self,
            element,
            job_url,
            locate_search_box_by,
            search_box_locator,
            job_element_locator,
            link_prefix,
            keyword,
            next_button_element=None
            ):
        self.browser.get(job_url)
        self.locate_and_search(locate_search_box_by, search_box_locator, keyword)
        job_list = self.get_list_of_jobs(element, job_element_locator, link_prefix, next_button_element)
        # print("job_list", len(job_list))
        self.save_to_excel(element, job_list)

    def save_to_excel(self, element, job_list):
        time_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "Jobs": job_list,
            "Date Added": [time_added]*len(job_list),
            "Applied": [False]*len(job_list)
        }
        df = pd.DataFrame(data)
        # print("df", len(df))
        try:
            df_old_data = pd.read_excel("output.xlsx", sheet_name=element)
        except Exception as e:
            print(e)
            print("Creating the empty excel sheet now.")
            df_old_data = pd.DataFrame({'Jobs': [], 'Date Added': [], 'Applied': []})

        finalmerged = pd.concat([df_old_data, df], join='outer')
        removed_duplicates = finalmerged.drop_duplicates(['Jobs'])

        try:
            with pd.ExcelWriter(
                    "output.xlsx",
                    engine="openpyxl",
                    mode="a",
                    if_sheet_exists="overlay"
                ) as writer:
                    removed_duplicates.to_excel(writer, sheet_name=element, index=False)
        except FileNotFoundError:
            removed_duplicates.to_excel("output.xlsx", sheet_name=element, index=False)

        print(f"Jobs saved to output.xlsx: {len(removed_duplicates)} from {element}")

    def get_list_of_jobs(self, element, job_element_locator, link_prefix, next_button_element=None):
        job_list = []
        raw_jobs_array = []
        # try:
            # next_button_locator_strategy = getattr(By, next_button_element['locate_by'].split(".")[1])
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        temp_raw_jobs_array =soup.select(job_element_locator)
        raw_jobs_array.extend(temp_raw_jobs_array)
        # print(len(raw_jobs_array))
        wait = WebDriverWait(self.browser, 5)
            # next_button = wait.until(
            #     EC.element_to_be_clickable((next_button_locator_strategy, next_button_element['locator'])),  # Replace with actual ID or locator
            #     EC.presence_of_element_located((next_button_locator_strategy, next_button_element['locator']))  # Replace with actual ID or locator
            # )
            # print("Next button clickable")
            # next_button.click()
            # time.sleep(5)
        # except Exception as e:
        #     print(e)
        #     print("Reached end of pages")
        #     break
        for job_element in raw_jobs_array:
            job_list.append(link_prefix + job_element.get('href'))
        # print("job_list", len(job_list))
        return job_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Toggle headless mode for Selenium WebDriver.")
    parser.add_argument(
        "--headless",
        action="store_true",  # Flag argument (True if specified, False otherwise)
        help="Run the browser in headless mode.",
    )
    args = parser.parse_args()
    keyword = "Reliability"
    job_scraper = JobScraper(args.headless)

    link_dict = json.load(open('input.json', 'r'))

    for element in link_dict.keys():
        print(link_dict[element]['url'])
        job_scraper.search_website_for_jobs(
            element,
            link_dict[element]['url'],
            link_dict[element]['locate_search_box_by'],
            link_dict[element]['search_box_locator'],
            link_dict[element]['job_element_locator'],
            link_dict[element]['link_prefix'],
            keyword,
            link_dict[element]['next_button'] if 'next_button' in link_dict[element] else None
        )
    job_scraper.browser.quit()
