import pandas as pd
import yfinance as yf

tickers = ['AAPL', 'GOOG', 'NVDA']

df = pd.DataFrame()

for ticker in tickers:
    df_temp = yf.download(ticker, start='2025-01-01', end='2026-03-19').reset_index()
    df_temp.columns = df_temp.columns.droplevel('Ticker')
    df_temp['Ticker'] = ticker
    df_temp = df_temp[['Ticker', 'Date', 'Close']]
    df = pd.concat([df, df_temp])

print(df)
