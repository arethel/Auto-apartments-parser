from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# URL of the webpage you want to open
url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Bfilter_enum_furniture%5D%5B0%5D=yes&search%5Bfilter_float_price%3Ato%5D=2100&search%5Border%5D=created_at%3Adesc&search%5Bphotos%5D=1#857141460'  # Replace with the desired URL

# Open the webpage
driver.get(url)

def get_element_by_testid(driver, test_id):
    try:
        element = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{test_id}"]')
        return element
    except Exception as e:
        print(f"Error: {e}")
        return None

import requests

# Replace 'YOUR_BOT_TOKEN' with the actual token you received from BotFather
BOT_TOKEN = '6395224777:AAG-FGvd4GWkMvcB8n9_WAj3yw5hhD4FgwY'

# URL for interacting with the Telegram Bot API
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

def get_users():
    response = requests.get(BASE_URL + 'getUpdates')
    # print(response.content)
    users = set()
    if 'result' in response.json():
        for update in response.json()['result']:
            users.add(update['message']['chat']['id'])
    return list(users)

def send_news_to_users(news):
    users = get_users()
    # print(users)
    for user_id in users:
        send_message(user_id, news)

def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.json()


# send_news_to_users("Hi!")

last_id = -1
while True:
    time.sleep(60)
    aparetments_div = get_element_by_testid(driver, 'listing-grid')
    if aparetments_div:
    # Find all <div> elements within the main element
        div_elements = aparetments_div.find_elements(By.CSS_SELECTOR, f'[data-cy="l-card"]')
        # Create a list to store the text content of the <div> elements
        div_ids = []

        # Iterate through the <div> elements and add their text content to the list
        for div_element in div_elements:
            div_ids.append(int(div_element.get_attribute('id')))
        
        if last_id != div_ids[3]:
            if last_id != -1:
                apartment_div = driver.find_element(By.ID, div_ids[3])
                apartment_div = apartment_div.find_element(By.CLASS_NAME, 'css-rc5s2u')
                apartment_link = apartment_div.get_attribute('href')
                send_news_to_users(apartment_link)
            last_id = div_ids[3]
        
    else:
        print("Main element not found")
        print(aparetments_div)
    driver.refresh()  # Reload the page
# Close the browser window when done
# driver.quit()