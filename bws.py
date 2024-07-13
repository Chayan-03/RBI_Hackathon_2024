# this is a prototype for a basic web scraper
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(soup):
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links

def main():
    url = input("Enter the URL to scrape: ")
    html_content = fetch_html(url)
    if html_content:
        soup = parse_html(html_content)
        print(soup.prettify())

        links = extract_links(soup)
        print("Extracted links:")
        for link in links:
            print(link)
    else:
        print("Failed to retrieve the webpage. Please check the URL and try again.")

if __name__ == "__main__":
    main()

