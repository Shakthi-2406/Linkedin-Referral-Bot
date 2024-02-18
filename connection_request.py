from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

load_dotenv()

connection_people_link = 'https://www.linkedin.com/search/results/people/?currentCompany=%5B%229252341%22%2C%221441%22%2C%221038%22%2C%221035%22%2C%221009%22%2C%223185%22%2C%221068%22%2C%221028%22%2C%221123%22%2C%2229352%22%2C%221815218%22%2C%223608%22%2C%221043%22%2C%22165158%22%2C%221090%22%2C%22321062%22%2C%22309694%22%2C%221025%22%2C%221076967%22%2C%221145485%22%2C%2211781910%22%2C%221426%22%2C%221466%22%2C%2220226%22%2C%222268557%22%2C%22229433%22%2C%222580522%22%2C%222988%22%2C%223477522%22%2C%2238373%22%2C%223843%22%2C%22487488%22%2C%225383634%22%2C%2271301545%22%2C%2278792265%22%2C%228074624%22%2C%2289599097%22%2C%22903031%22%2C%229390173%22%5D&keywords=talentacquisition&network=%5B%22S%22%2C%22O%22%5D&origin=FACETED_SEARCH&page=0&sid=u%3AP'
USERNAME_OR_EMAIL = 'shakthisri504@gmail.com' # add your email id
PASSWORD = 'ADD YOUR PASSWORD AND REMOVE LINE 14'
PASSWORD = os.getenv('PASSWORD')
LOGIN_URL = 'https://www.linkedin.com/login'
connections_sent = 0
driver = None

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
        time.sleep(10)
    except TimeoutException:
        driver.execute_script("window.stop();")

def load_connection_requests():
    global connection_people_link
    driver.set_page_load_timeout(30)
    try:
        driver.get(connection_people_link)
    except TimeoutException:
        driver.execute_script("window.stop();")
    time.sleep(2)


def send_without_a_note():
    global connections_sent
    send_without_note = driver.find_element(By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1')
    send_without_note.click()
    connections_sent += 1


def send_connection_requests():
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')))
    people = driver.find_elements(By.CLASS_NAME, 'artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')
    for connect_btn in people:
        # skip the premium ones
        # WebDriverWait(driver, 15).until(EC.element_to_be_clickable(connect_btn))
        option = connect_btn.find_element(By.CLASS_NAME, 'artdeco-button__text').text
        if option != 'Connect':
            continue
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(connect_btn))
        connect_btn.click()
        send_without_a_note()

def move_to_next_page(curr_page_number):
    global connection_people_link
    connection_people_link = connection_people_link.replace(f'page={curr_page_number}',
                                                            f'page={curr_page_number+1}')

def connect_with_people():
    global connections_sent
    curr_page_number = 0

    while True:
        move_to_next_page(curr_page_number)
        load_connection_requests()
        send_connection_requests()
        curr_page_number += 1
        print(f"Requests sent : {connections_sent}")


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)

    login()

    while True:
        connect_with_people()
    