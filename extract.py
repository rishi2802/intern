import requests
from bs4 import BeautifulSoup
import re
import time

def get_emails_from_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract email addresses using a regular expression
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
        return emails

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return []

def main():
    main_page_url = 'http://quotes.toscrape.com'

    try:
        response = requests.get(main_page_url)
        response.raise_for_status()

        main_soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the links on the main page
        links = main_soup.find_all('a', href=True)

        for link in links:
            # Construct the absolute URL for the linked page
            linked_page_url = link['href']
            if not linked_page_url.startswith('http'):
                linked_page_url = main_page_url + linked_page_url

            # Get emails from the linked page
            linked_emails = get_emails_from_page(linked_page_url)

            if linked_emails:
                print(f"Emails from {linked_page_url}: {linked_emails}")
            else:
                print(f"No emails found on {linked_page_url}")

            # Add a delay between requests to avoid being blocked or rate-limited
            #time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {main_page_url}: {e}")

if __name__ == "__main__":
    main()
