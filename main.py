from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import PyPDF2
import io
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

from filters import fillFilters, clickButton, filterPDF

url = "https://uottawa.syntosolution.com/general-directory"

options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/brave"
driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(0.5)

fillFilters(driver)
time.sleep(0.5)

for i in range(25):
    
    filterPDF(driver)
    time.sleep(0.5)

    nextExists = driver.find_element(By.XPATH, '//button[@aria-label="paginatorNextPage"]')
    if not (nextExists.is_displayed() and nextExists.is_enabled()):
        break

    else:       
        clickButton('//button[contains(@aria-label, "paginatorNextPage")]', "paginatorNextPage", driver)
        time.sleep(0.5)

driver.quit()