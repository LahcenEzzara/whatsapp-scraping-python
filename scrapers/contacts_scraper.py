import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get the Chrome user data directory from environment variable
chrome_user_data_dir = r'C:\Users\Lahcen\AppData\Local\Google\Chrome\User Data\Profile 1'
chrome_driver_path = r'C:\Store\ChromeDriver\chromedriver.exe'

# Set up Chrome options
print("Setting up Chrome options...")
chrome_options = Options()
chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
chrome_options.add_argument('--profile-directory=Default')

# Start the WebDriver
print("Starting WebDriver...")
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://web.whatsapp.com')

# Wait for the user to scan the QR code or WhatsApp Web to load
input("Press Enter after WhatsApp Web has fully loaded...")


def scrape_contact_numbers():
    """
    Scrape contact numbers from WhatsApp Web.

    This function waits for the chat list to load and then extracts the contact numbers
    from the chat list. It returns a list of contact numbers.

    Returns:
        list: A list of contact numbers as strings.
    """
    contact_numbers = []
    try:
        print("Waiting for chats to load...")
        # Wait for the chats to load
        chat_list = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@id="pane-side"]//span[@title]')
            )
        )
        print("Chats loaded successfully.")

        # Iterate through the chat list and extract contact numbers
        print("Scraping contact numbers...")
        for idx, chat in enumerate(chat_list, start=1):
            contact_number = chat.get_attribute('title')
            # Ignore special characters
            if contact_number.startswith('‪') or contact_number.startswith('‫'):
                continue
            contact_numbers.append(contact_number)
            print(f"Contact {idx}: {contact_number}")

        print("Scraping completed successfully.")
        return contact_numbers
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []


try:
    print("Starting contact scraping process...")
    # Scrape contact numbers
    contact_numbers = scrape_contact_numbers()

    # Save contact numbers to a CSV file
    print("Saving contact numbers to CSV file...")
    csv_file = 'contact_numbers.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow(['Contact Number'])
        for number in contact_numbers:
            writer.writerow([number])
    print(f"Contact numbers saved to {csv_file} successfully.")
finally:
    # Ensure the WebDriver is closed properly
    print("Closing WebDriver...")
    driver.quit()
    print("WebDriver closed.")
