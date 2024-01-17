import requests
from bs4 import BeautifulSoup
import re
import time

def get_emails_from_page(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract email addresses from mailto links
        email_links = soup.find_all('a', href=re.compile(r'mailto:'))
        emails = [re.sub(r'^mailto:', '', link['href']) for link in email_links]

        # Extract email addresses from elements with data-email attribute
        emails += [email['data-email'] for email in soup.find_all(class_='attorney-email')]

        return emails

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return []

def save_emails_to_file(emails, filename='extracted_emails.txt'):
    with open(filename, 'w') as file:
        for email in emails:
            file.write(email + '\n')

def main():
    main_page_url = 'https://www.mwe.com/people/'

    # Create a session to persist cookies
    with requests.Session() as session:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'DNT': '1',  # "Do Not Track" header
            # Add more headers if needed
        }

        try:
            response = session.get(main_page_url, headers=headers)
            response.raise_for_status()

            main_soup = BeautifulSoup(response.content, 'html.parser')
            # Find all the links on the main page
            links = main_soup.find_all('a', href=True)

            extracted_emails = []

            for link in links:
                # Construct the absolute URL for the linked page
                linked_page_url = link['href']
                if not linked_page_url.startswith('http'):
                    linked_page_url = main_page_url + linked_page_url

                # Get emails from the linked page
                linked_emails = get_emails_from_page(linked_page_url, session)

                if linked_emails:
                    print(f"Emails from {linked_page_url}: {linked_emails}")
                    extracted_emails.extend(linked_emails)
                else:
                    print(f"No emails found on {linked_page_url}")

                # Add a delay between requests to avoid being blocked or rate-limited
                time.sleep(1)

            # Save extracted emails to a file
            save_emails_to_file(extracted_emails)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {main_page_url}: {e}")

if __name__ == "__main__":
    main()
