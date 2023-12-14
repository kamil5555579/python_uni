from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

options = Options()
#options.add_argument('--headless')

service = Service('python_naukowy/webdriver/chromedriver.exe')

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.nofluffjobs.com/pl')
cookies_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
cookies_button.click()

country_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mat-dialog-0 > div > div > div > div.info-hard__region-picker.mt-1.mt-sm-5 > div.row > div:nth-child(1) > button')))
country_button.click()

confirm_country_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mat-dialog-0 > div > div > div > div.info-hard__region-picker.mt-1.mt-sm-5 > div.tw-flex.tw-justify-center.mt-3.mt-sm-4 > button.tw-btn.tw-btn-xl.tw-btn-primary.mn-3')))
confirm_country_button.click()

search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mat-chip-list-0 > div')))
search_button.click()
search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-chip-list-wrapper > input')))

search_field.send_keys('Warszawa')
search_field.send_keys(Keys.ENTER)
search_field.send_keys('junior')
search_field.send_keys(Keys.ENTER)

techologies = ['python', 'java', 'c++', 'sql']
jobs = []
for techology in techologies:
    search_field.send_keys(techology)
    search_field.send_keys(Keys.ENTER)
    posting_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'nfj-postings-list')))
    posts = posting_list.find_elements(By.CSS_SELECTOR, 'nfj-posting-item-title')
    titles = [post.find_element(By.CSS_SELECTOR, 'h3') for post in posts]
    companies = [post.find_element(By.CSS_SELECTOR, 'span') for post in posts]
    for title, company in zip(titles, companies):
        jobs.append({'title': title.text, 'company': company.text, 'techology': techology})
    search_button.click()
    remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mat-chip-list-0 > div > mat-chip:nth-child(2) > span.mat-chip-remove.ng-star-inserted > inline-icon > svg')))
    remove_button.click()

with open('python_naukowy/jobs2.json', 'w') as f:
    json.dump(jobs, f, indent=4)

driver.close()