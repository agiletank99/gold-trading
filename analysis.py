import os
import yfinance as yf
import pandas as pd

def get_market_data(ticker="GC=F"):
    try:
        data = yf.download(ticker, period="7d", interval="1h", progress=False)
        if data.empty:
            return "Dati vuoti da yfinance."
        try:
    ultimo_prezzo = float(data['Close'].iloc[-1])
    return f"Ultimo prezzo Close per l'oro: {ultimo_prezzo:.2f}"
except (ValueError, TypeError):
    return "Dati ricevuti da yfinance non sono numerici."
    except Exception as e:
        return f"Errore yfinance: {e}"

def analyze_market():
    return get_market_data()
