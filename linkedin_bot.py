from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

load_dotenv()

USERNAME_OR_EMAIL = 'shakthisri504@gmail.com'
PASSWORD = 'ADD YOUR PASSWORD AND REMOVE LINE 12'
PASSWORD = os.getenv('PASSWORD')
LOGIN_URL = 'https://www.linkedin.com/login'
referrals_sent = 0
driver = None
all_people_url = None

def login():
    try:
        driver.get(LOGIN_URL)
    except TimeoutException:
        driver.execute_script("window.stop();")    
    time.sleep(6)
    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys(USERNAME_OR_EMAIL)
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(PASSWORD)
    signin_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
    driver.set_page_load_timeout(200)
    try:
        signin_button.click()
    except TimeoutException:
        driver.execute_script("window.stop();")


def load_company_people(company_name):
    global all_people_url
    driver.set_page_load_timeout(30)
    try:
        driver.get(f"https://www.linkedin.com/search/results/all/?keywords={company_name}&origin=GLOBAL_SEARCH_HEADER&sid=HQT")
    except TimeoutException:
        driver.execute_script("window.stop();")
    time.sleep(2)
    all_people = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results__cluster-bottom-banner')))
    all_people.click()
    all_people_url = driver.current_url

def send_message_and_close(content):
    global referrals_sent
    add_a_note = driver.find_element(By.CLASS_NAME, 'artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view.mr1')
    add_a_note.click()
    text_area = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ember-text-area.ember-view.connect-button-send-invite__custom-message.mb3')))
    text_area.send_keys(content)
    send_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1')))
    send_btn.click()
    referrals_sent += 1

def send_message_in_current_page(content):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')))
    people = driver.find_elements(By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')
    for connect_btn in people:
        # skip the premium ones
        # WebDriverWait(driver, 15).until(EC.element_to_be_clickable(connect_btn))
        option = connect_btn.find_element(By.CLASS_NAME, 'artdeco-button__text').text
        print(option)
        if option != 'Connect':
            continue
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(connect_btn))
        connect_btn.click()
        send_message_and_close(content)

def move_to_next_page(page_number):
    global all_people_url
    driver.get(f"{all_people_url}&page={page_number}")


def get_input_and_send_referrals():
    global referrals_sent
    referrals_sent = 0

    company = input("Enter the company name: ")
    role = input("Enter the role: ")
    job_id = input("Enter the job id: ")
    referrals_needed = int(input("Enter the number of referrals you want: "))

    load_company_people(company)
    next_page = 2

    content = f'''Hey!\nI'm BTech CSE'24 grad.Am applying to {role.title()} at {company.title()}. Can you please give me a referral if you feel that am worth for it?\nshakthi.btech.cse24@gmail.com'''

    if len(job_id) > 4:
        content += f'\nJOB ID - {job_id}'

    while referrals_sent < referrals_needed:
        send_message_in_current_page(content)
        move_to_next_page(next_page)
        next_page += 1
    print(f"Referrals sent : {referrals_sent}")


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)

    login()

    while True:
        get_input_and_send_referrals()
    