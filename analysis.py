import os
import yfinance as yf
import pandas as pd

def get_market_data(ticker="GC=F"):
    try:
        data = yf.download(ticker, period="7d", interval="1h", progress=False)
        if data.empty:
            return "Dati vuoti da yfinance."
        return f"Ultimo prezzo Close per l'oro: {data['Close'].iloc[-1]:.2f}"
    except Exception as e:
        return f"Errore yfinance: {e}"

def analyze_market():
    return get_market_data()