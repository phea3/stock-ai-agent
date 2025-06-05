import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.widgets as widgets
import requests

class StockAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def get_stock_info(self, stock, market):
        if market == 'NASDAQ':
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&outputsize=compact&apikey={self.api_key}'
        else:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}.{market}&outputsize=compact&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        return data 
    
class StockAnalyzer:
    def __init__(self):
        pass

    def json_to_dataframe(self, json_data, stock, market):
        if 'Time Series (Daily)' not in json_data:
            print(f"Error: 'Time Series (Daily)' not found for {stock} in {market}")
            print("API Response:", json_data)
            return None  # Return None on failure

        time_series_data = json_data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(time_series_data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        # Convert all columns to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])

        return df

    def plot_stock_data(self, df, stock_symbol, market, image_path):
        plt.figure(figsize=(16, 10))

        # Plot Closing Price
        plt.subplot(3, 1, 1)
        plt.plot(df.index, df['4. close'], label=f'{stock_symbol} Closing Price ({market})', color='blue')
        plt.title(f'{stock_symbol} Stock Performance ({market})')
        plt.xlabel('Date (IST)')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Plot Volume
        plt.subplot(3, 1, 2)
        plt.bar(df.index, df['5. volume'], label=f'{stock_symbol} Volume ({market})', color='green', width=2)
        plt.xlabel('Date (IST)')
        plt.ylabel('Volume')
        plt.legend()
        plt.grid(True)

        # Plot Moving Averages
        plt.subplot(3, 1, 3)
        df['MA_7'] = df['4. close'].rolling(window=7).mean()
        df['MA_20'] = df['4. close'].rolling(window=20).mean()
        plt.plot(df.index, df['4. close'], label=f'{stock_symbol} Closing Price ({market})', color='blue', alpha=0.7)
        plt.plot(df.index, df['MA_7'], label='7-Day MA', color='orange')
        plt.plot(df.index, df['MA_20'], label='20-Day MA', color='red')
        plt.xlabel('Date Month(IST)')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Date formatting for all subplots
        for ax in plt.gcf().axes:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=[0]))  # Mondays
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gcf().autofmt_xdate()

        # Remove cursor widget as it won't work in Streamlit
        # cursor = widgets.Cursor(plt.gca(), color='red', linewidth=1)

        plt.tight_layout()
        plt.savefig(image_path) 
        # plt.show()  # Remove this in Streamlit environment
