# WhatsApp Scraping Project

This project includes several Python scripts to scrape contacts and chat messages from WhatsApp Web using Selenium. 

## Prerequisites

1. **Python**: Make sure you have Python 3.6 or higher installed.
2. **Google Chrome**: Ensure you have Google Chrome installed.
3. **ChromeDriver**: Download ChromeDriver from the official website:
   [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/#stable)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/whatsapp-scraper.git
    cd whatsapp-scraper
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the ChromeDriver**:
    - Download the ChromeDriver from the link above.
    - Extract the downloaded file.
    - Move the `chromedriver` executable to a directory that is in your system's `PATH`.

4. **Configure the environment variables**:
    - Create a `.env` file in the project root directory.
    - Add the following content to the `.env` file:
      ```ini
      CHROME_USER_DATA_DIR=path_to_your_chrome_user_data
      ```

## Usage

### Scraping Contacts

1. **Script**: `contacts_scraper.py`
2. **Description**: Scrapes contact numbers from WhatsApp Web.
3. **Run**:
    ```bash
    python contacts_scraper.py
    ```

### Scraping a Single Chat

1. **Script**: `single_chat_scraper.py`
2. **Description**: Scrapes messages from a specific WhatsApp chat.
3. **Configuration**: Edit the script to set the `chat_name` variable to the name of the chat you want to scrape.
4. **Run**:
    ```bash
    python single_chat_scraper.py
    ```

### Scraping Multiple Chats from a CSV

1. **Script**: `csv_multi_chat_scraper.py`
2. **Description**: Scrapes messages from multiple WhatsApp chats listed in a CSV file.
3. **Configuration**: Ensure you have a `contact_numbers.csv` file with chat names, one per line.
4. **Run**:
    ```bash
    python csv_multi_chat_scraper.py
    ```

### Scraping Multiple Chats Specified in the Script

1. **Script**: `multi_chat_scraper.py`
2. **Description**: Scrapes messages from multiple WhatsApp chats specified in the script.
3. **Configuration**: Edit the script to update the `chat_names` list with the names of the chats you want to scrape.
4. **Run**:
    ```bash
    python multi_chat_scraper.py
    ```

## Notes

- Ensure that you have logged into WhatsApp Web on Chrome before running the scripts.
- The scripts will prompt you to scan the QR code if you are not logged in.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
