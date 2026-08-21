import yfinance as yf
import pandas as pd
from datetime import datetime
import time


def get_stock_price(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d", interval="1m")

        if data.empty:
            return None

        latest = data.iloc[-1]

        return {
            "Ticker": ticker_symbol,
            "Date": latest.name.strftime("%Y-%m-%d %H:%M:%S"),
            "Open": latest["Open"],
            "High": latest["High"],
            "Low": latest["Low"],
            "Close": latest["Close"],
            "Volume": latest["Volume"]
        }

    except Exception as e:
        print(f"Error retrieving price for {ticker_symbol}: {e}")
        return None


def get_financial_metrics(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        return {
            "Ticker": ticker_symbol,
            "Company": info.get("longName"),
            "Sector": info.get("sector"),
            "Industry": info.get("industry"),
            "Market Cap": info.get("marketCap"),
            "Enterprise Value": info.get("enterpriseValue"),
            "Revenue": info.get("totalRevenue"),
            "EBITDA": info.get("ebitda"),
            "Net Income": info.get("netIncomeToCommon"),
            "EPS": info.get("trailingEps"),
            "P/E": info.get("trailingPE"),
            "Forward P/E": info.get("forwardPE"),
            "P/B": info.get("priceToBook"),
            "EV/EBITDA": info.get("enterpriseToEbitda"),
            "ROE": info.get("returnOnEquity"),
            "ROA": info.get("returnOnAssets"),
            "Revenue Growth": info.get("revenueGrowth"),
            "Earnings Growth": info.get("earningsGrowth"),
            "Debt to Equity": info.get("debtToEquity"),
            "Current Ratio": info.get("currentRatio"),
            "Dividend Yield": info.get("dividendYield")
        }

    except Exception as e:
        print(f"Error retrieving fundamentals for {ticker_symbol}: {e}")
        return None


def analyze_stock(ticker_symbol):
    print(f"Collecting data for {ticker_symbol}...")

    price_data = get_stock_price(ticker_symbol)

    time.sleep(1)

    financial_data = get_financial_metrics(ticker_symbol)

    if price_data is None and financial_data is None:
        return None

    combined_data = {}

    if price_data:
        combined_data.update(price_data)

    if financial_data:
        combined_data.update(financial_data)

    combined_data["Scraped At"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return combined_data


def scrape_stocks(tickers):
    results = []

    for ticker in tickers:
        data = analyze_stock(ticker)

        if data:
            results.append(data)

    return pd.DataFrame(results)


def save_to_csv(dataframe, filename="stock_analysis.csv"):
    dataframe.to_csv(filename, index=False)
    print(f"Data saved successfully to: {filename}")


def main():

    tickers = [
        "RELIANCE.NS",
        "TCS.NS",
        "HDFCBANK.NS",
        "INFY.NS"
    ]

    stock_dataframe = scrape_stocks(tickers)

    if not stock_dataframe.empty:

        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 200)

        print(stock_dataframe)

        save_to_csv(stock_dataframe)

    else:
        print("No stock data was collected.")


if __name__ == "__main__":
    main()



