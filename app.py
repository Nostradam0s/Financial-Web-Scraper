
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.5013882 Safari/537.36'}

urls =[
    'https://groww.in/us-stocks/nke',
    'https://groww.in/us-stocks/ko',
    'https://groww.in/us-stocks/msft',
    'https://groww.in/stocks/m-india-ltd',
    'https://groww.in/us-stocks/axp',
    'https://groww.in/us-stocks/amgn',
    'https://groww.in/us-stocks/aapl',
    'https://groww.in/us-stocks/ba',
    'https://groww.in/us-stocks/csco',
    'https://groww.in/us-stocks/gs',
    'https://groww.in/us-stocks/ibm',
    'https://groww.in/us-stocks/intc',
    'https://groww.in/us-stocks/jpm',
    'https://groww.in/us-stocks/mcd',
    'https://groww.in/us-stocks/crm',
    'https://groww.in/us-stocks/vz',
    'https://groww.in/us-stocks/v',
    'https://groww.in/us-stocks/wmt',
    'https://groww.in/us-stocks/dis'
]


def get_stock_data(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        # Company name
        company = soup.find('h1', {'class': 'usph14Head displaySmall'})
        if company:
            company = company.text.strip()
        else:
            company = "N/A"

        # Price (handle duplicate class)
        price_tags = soup.find_all('span', {'class': 'uht141Pri contentPrimary displayBase'})
        price= price_tags[0].text.strip() if price_tags else "N/A"

        # Change (%)
        change_tags = soup.find_all('span', {'class': 'uht141Day bodyBaseHeavy contentNegative'})
        if not change_tags:
            # Try positive class
         change_tags = soup.find_all('span', {'class': 'uht141Day bodyBaseHeavy contentPositive'})
         change = change_tags[0].text.strip() if change_tags else "N/A"

         # Volume
        volume_table = soup.find('table', {'class': 'tb10Table col l5'})
        volume = volume_table.find_all('td')[1].text.strip() if volume_table else "N/A"

        return {
            'Company': company,
            'Price': price,
            'Change': change,
            'Volume': volume,
            'URL': url
         }
    except Exception as e:
      print(f"Error scraping {url}: {e}")
    return None

# Loop through URLs
for url in urls:
    data = get_stock_data(url)
    if data:
        print(data)
        print('-' * 50)
