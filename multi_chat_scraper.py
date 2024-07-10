import os
import csv
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
print("Loading environment variables...")
load_dotenv()

# Get the Chrome user data directory from environment variable
chrome_user_data_dir = os.getenv('CHROME_USER_DATA_DIR')
if not chrome_user_data_dir:
    raise ValueError("CHROME_USER_DATA_DIR environment variable not set")
print("Environment variables loaded successfully.")

# Set up Chrome options
print("Setting up Chrome options...")
chrome_options = Options()
chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
chrome_options.add_argument('--profile-directory=Default')

# Start the WebDriver
print("Starting WebDriver...")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://web.whatsapp.com')

# Wait for the user to scan the QR code or WhatsApp Web to load
input("Press Enter after WhatsApp Web has fully loaded...")


def scrape_whatsapp_chat(chat_name):
    """
    Scrape messages from a specific WhatsApp chat.

    Args:
        chat_name (str): The name of the chat to scrape.

    Returns:
        list: A list of messages, each containing a timestamp, chat name, and message text.
    """
    print(f"Starting scraping for chat: {chat_name}")
    try:
        # Search for the chat
        print("Searching for the chat...")
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.click()
        search_box.send_keys(chat_name)
        time.sleep(3)  # Wait for search results to load

        # Click on the chat
        print("Selecting the chat...")
        chat = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//span[@title="{chat_name}"]'))
        )
        chat.click()
        time.sleep(3)  # Wait for chat to load

        # Scroll to the top to load all messages
        print("Scrolling to load all messages...")
        last_height = driver.execute_script(
            "return document.querySelector('div.copyable-area').scrollHeight")
        while True:
            driver.execute_script(
                "document.querySelector('div.copyable-area').scrollTo(0, 0);")
            time.sleep(1)  # Reduced wait time for quicker scrolling
            new_height = driver.execute_script(
                "return document.querySelector('div.copyable-area').scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract messages
        print("Extracting messages...")
        messages = driver.find_elements(
            By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')

        chat_data = []
        for idx, message in enumerate(messages, start=1):
            try:
                text_elements = message.find_elements(
                    By.XPATH, './/span[@class="_ao3e selectable-text copyable-text"]//span')
                if text_elements:
                    text = " ".join(
                        [element.text for element in text_elements])
                    timestamp = message.find_element(
                        By.XPATH, './/div[@data-pre-plain-text]').get_attribute('data-pre-plain-text')
                    chat_data.append([timestamp, chat_name, text])
                    print(f"Message {idx}: {timestamp} - {text}")
            except Exception as e:
                print(f"Error extracting message {idx}: {e}")
                continue

        print(f"Scraping completed for chat: {chat_name}")
        return chat_data
    except Exception as e:
        print(f"An error occurred while scraping chat {chat_name}: {e}")
        return []


# List of chat names you want to scrape
chat_names = ["Lahcen Ezzara", "Achraf ENSIAS", "+212 619-736686"]

# Create or open the CSV file and write headers
csv_file = 'all_chat.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Chat Name', 'Message'])

# Scrape data for each chat and append to the CSV file
for chat_name in chat_names:
    print(f"Initiating chat scraping for '{chat_name}'...")
    chat_data = scrape_whatsapp_chat(chat_name)
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(chat_data)

    # Click the home button to return to the chat list and clear the search
    try:
        print("Returning to the home screen...")
        home_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@aria-label="Cancel search"]'))
        )
        home_button.click()
        time.sleep(2)  # Reduced wait time for quicker navigation
    except Exception as e:
        print(f"Error returning to the home screen after scraping {
              chat_name}: {e}")

print(f"Chat data saved to {csv_file}")

# Close the WebDriver
print("Closing WebDriver...")
driver.quit()
print("WebDriver closed.")
