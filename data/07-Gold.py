import pandas as pd
import yfinance as yf

# --- Yahoo Finance: gold price (GC=F) from 2025-01-01
df = yf.download("GC=F", start="2025-01-01", end="2026-03-09")
df = df[["Close"]].reset_index()
df.columns = df.columns.droplevel("Ticker")
df = df.rename(columns={"Close": "XAUUSD"})

# 1 troy ounce = 31.1035g, 1 baht-weight = 15.244g
# ~2.04 baht-weight per troy ounce
# THB gold price per baht-weight = (XAUUSD / 2.04) * 32
df["THB"] = (df["XAUUSD"] / 2.04) * 32

df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
df = df[["Date", "XAUUSD", "THB"]]
df["XAUUSD"] = df["XAUUSD"].round(2)
df["THB"] = df["THB"].round(2)

print("=== Gold Price: XAUUSD & THB per baht-weight ===")
print(df.to_string(index=False))
