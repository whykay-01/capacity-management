import requests
from bs4 import BeautifulSoup
import os

# Define the target website URL
website_url = input("Please input the link to crawl: ") 

# Send a GET request to the homepage
response = requests.get(website_url)

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the links on the homepage or any specific section of the website
links = soup.find_all('a')

# Create a directory to store the HTML files
output_dir = 'html_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Download and save each HTML file, handling errors
for link in links:
    # Get the URL of each link
    page_url = link['href']
    print(link)
    
    try:
        # Send a GET request to the page
        page_response = requests.get(page_url)
        
        # Create a BeautifulSoup object to parse the HTML
        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        
        # Save the HTML content as a file
        filename = os.path.join(output_dir, f'{link.text}.html')
        with open(filename, 'w') as file:
            file.write(page_soup.prettify())
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while requesting {page_url}: {e}")
        continue
