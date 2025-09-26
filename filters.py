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

def clickButton(identifier, name, driver):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, identifier))
        )

        button.click()
        print(f"Clicked {name} button.")

    except Exception as e:
        print(f"{name} button not found:", e)
    
    time.sleep(0.5)

def escape(driver):
    escape = driver.find_element(By.CSS_SELECTOR, "mat-select")
    escape.send_keys(Keys.ESCAPE)
    time.sleep(0.5)

def fillFilters(driver):
    clickButton("//button[contains(., 'Filters')]", 'Filters', driver)
    clickButton("//mat-form-field[contains(., 'Select Faculty')]", 'Select Faculty', driver)
    # clickButton("//mat-option[contains(., ' Faculty of Engineering ')]", ' Faculty of Engineering ', driver)
    clickButton("//mat-option[contains(., ' Faculty of Science ')]", ' Faculty of Science ', driver)

    
    escape(driver)

    clickButton("//button[contains(., 'Filters')]", 'Filters', driver)
    clickButton("//mat-form-field[contains(., 'Select Level of Study')]", 'Select Level of Study', driver)
    clickButton("//mat-option[contains(., ' Undergraduate Studies ')]", ' Undergraduate Studies ', driver)

    escape(driver)

    clickButton("//button[contains(., 'Filters')]", 'Filters', driver)
    clickButton("//mat-form-field[contains(., 'Select Legal Status')]", 'Select Legal Status', driver)
    clickButton("//mat-option[contains(., ' Canadian Citizen ')]", ' Canadian Citizen ', driver)

    escape(driver)

    clickButton("//button[contains(., 'Filters')]", 'Filters', driver)
    clickButton("//mat-form-field[contains(., 'Select Application Requirement')]", 'Select Application Requirement', driver)
    clickButton("//mat-option[contains(., ' Application Required ')]", ' Application Required ', driver)

    escape(driver)

    clickButton("//button[contains(., 'Filters')]", 'Filters', driver)
    clickButton("//mat-form-field[contains(., 'Select Canadian Residency')]", 'Select Canadian Residency', driver)
    clickButton("//mat-option[contains(., ' Ontario Residence ')]", ' Ontario Residence ', driver)

    escape(driver)

    clickButton("//button[contains(., 'Filters')]", 'Filters', driver)
    clickButton("//button[contains(., ' Apply Filters (5) ')]", ' Apply Filters (5) ', driver)

def filterPDF(driver):
    pdf_links = []
    for a in driver.find_elements(By.XPATH, "//a[contains(., ' View Details ')]"):
        href = a.get_attribute("href")
        if href and href.endswith(".pdf"):
            pdf_links.append(href)

    output_file = "filtered.txt"
    # key_words = ['Biomedical', 'Chemical', 'Métis', 'welfare', "Francophone", "First Nation", 'sports', "athlete", 'French', 'soccer', 'women', 'woman', 'Gee-Gee', 'third', 'fourth', 'international', 'Indigenous', 'Jewish']
    key_words = ['Physics', 'Métis', 'welfare', "Francophone", "First Nation", 'sports', "athlete", 'French', 'soccer', 'Gee-Gee', 'third', 'fourth', 'international', 'Indigenous', 'Jewish']

    for link in pdf_links:        

        response = requests.get(link)

        with io.BytesIO(response.content) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            
            interested = True
            for word in key_words:
                if word in text:
                    interested = False

            if interested:
                with open(output_file, "a") as f:
                    f.write(link + "\n")