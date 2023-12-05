from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

load_dotenv()

USERNAME_OR_EMAIL = 'shakthisri504@gmail.com'
PASSWORD = 'ADD YOUR PASSWORD AND REMOVE LINE 12'
PASSWORD = os.getenv('PASSWORD')
LOGIN_URL = 'https://www.linkedin.com/login'
referrals_sent = 0

def login(driver):
    driver.get(LOGIN_URL)
    time.sleep(2)
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys(USERNAME_OR_EMAIL)
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(PASSWORD)
    signin_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
    signin_button.click()

def load_company_people(driver, company_name):
    driver.get(f"https://www.linkedin.com/search/results/all/?keywords={company_name}&origin=GLOBAL_SEARCH_HEADER&sid=HQT")
    time.sleep(2)
    all_people = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results__cluster-bottom-banner')))
    all_people.click()

def send_message_and_close(driver, content):
    add_a_note = driver.find_element(By.CLASS_NAME, 'artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view.mr1')
    add_a_note.click()
    text_area = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ember-text-area.ember-view.connect-button-send-invite__custom-message.mb3')))
    text_area.send_keys(content)
    send_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1')))
    send_btn.click()
    referrals_sent += 1

def send_message_in_current_page(driver, content):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')))
    people = driver.find_elements(By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')
    for connect_btn in people:
        # skip the premium ones
        option = connect_btn.find_element(By.CLASS_NAME, 'artdeco-button__text').text
        if option != 'Connect':
            continue
        connect_btn.click()
        send_message_and_close(driver, content)

def move_to_next_page(driver):
    next_page_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-pagination__button--next')))
    next_page_btn.click()

if __name__ == "__main__":
    referrals_needed = int(input("Enter the number of referrals you want: "))
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    login(driver)
    load_company_people(driver, 'siemens')
    while referrals_sent < referrals_needed:
        send_message_in_current_page(driver, "Hello I would like to connect")
        move_to_next_page(driver)
    print(f"Referrals sent : {referrals_sent}")