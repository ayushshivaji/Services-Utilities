from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def google_search(driver, query):
    driver.get("https://www.google.com/")
    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="q")
    submit_button = driver.find_element(by=By.NAME, value="btnK")

    text_box.send_keys("Selenium")
    time.sleep(5)
    submit_button.click()


def book_my_show(driver):
    driver.get("https://in.bookmyshow.com/explore/home/mumbai")
    # search_box = driver.find_element(by=By.ID, value="search-box")
    # search_box.send_keys("Coldplay")

if __name__ == '__main__':
    driver = webdriver.Chrome()
    # google_search(driver, "Selenium")
    book_my_show(driver)
    time.sleep(5)
    # driver.quit()
