import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

urls = [
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
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Company Name
        company_tag = soup.find('h1')
        company = company_tag.text.strip() if company_tag else 'N/A'

        # Price
        price_tag = soup.find('span', {'class': 'uht141Pri'})
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Change
        change_tag = soup.find('span', {'class': ['contentNegative', 'contentPositive']})
        change = change_tag.text.strip() if change_tag else 'N/A'

        # Initialize metrics dictionary
        metrics = {
            'Volume': 'N/A',
            'Market Cap': 'N/A',
            'P/E Ratio': 'N/A',
            'Dividend Yield': 'N/A',
            '52W High': 'N/A',
            '52W Low': 'N/A',
            'EPS': 'N/A',
            'ROE': 'N/A',
            'P/B Ratio': 'N/A',
            'Debt to Equity': 'N/A',
            'Face Value': 'N/A'
        }

        # Parse tables for financial metrics
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    label = cols[0].text.strip()
                    value = cols[1].text.strip()
                    for key in metrics.keys():
                        if key.lower() in label.lower():
                            metrics[key] = value

        return {
            'Company': company,
            'Price': price,
            'Change': change,
            **metrics,
            'URL': url
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Collect all data
all_data = []

for url in urls:
    print(f"Scraping: {url}")
    stock_data = get_stock_data(url)
    if stock_data:
        all_data.append(stock_data)
    time.sleep(2)  # polite delay

# Create and display the DataFrame
df = pd.DataFrame(all_data)

print("\nScraped Stock Data:\n")
print(df.to_string(index=False))

print("\nScraped Stock Data:\n")
print(df.to_string(index=False))



