import requests
from bs4 import BeautifulSoup
import re

# URL to scrape
base_url = 'https://www.gtlaw.com/en/professionals?letter=G'
url = f'{base_url}/page/1'

# Send a GET request to the first page
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data from the page
    for a_tag in soup.find_all('a', href=True):
        inner_page_url = f'{base_url}{a_tag["href"]}'
        
        # Send a GET request to the inner page
        inner_page_response = requests.get(inner_page_url)
        
        if inner_page_response.status_code == 200:
            inner_soup = BeautifulSoup(inner_page_response.content, 'html.parser')
            
            # Use a regular expression to find email addresses
            email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', inner_page_response.text)
            
            if email_addresses:
                print(f'Email addresses on {inner_page_url}:')
                for email in email_addresses:
                    print(email)
        else:
            print(f'Failed to retrieve inner page {inner_page_url}. Status code:', inner_page_response.status_code)
else:
    print('Failed to retrieve the first page. Status code:', response.status_code)
