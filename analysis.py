# analysis.py (versione a prova di errore)
import os
import yfinance as yf
import pandas as pd

def get_market_data(ticker="GC=F"):
    try:
        data = yf.download(ticker, period="7d", interval="1h", progress=False)

        # --- NUOVI CONTROLLI DI SICUREZZA ---
        
        # 1. Controlla se abbiamo ricevuto un DataFrame valido
        if not isinstance(data, pd.DataFrame) or data.empty:
            return "Errore: yfinance non ha restituito dati validi."

        # 2. Controlla se la colonna 'Close' esiste
        if 'Close' not in data.columns:
            return "Errore: La colonna 'Close' non è presente nei dati ricevuti."

        # 3. Estrai l'ultimo valore in modo sicuro
        last_close_value = data['Close'].iloc[-1]

        # 4. Prova a convertire il valore in un numero prima di formattarlo
        try:
            price_as_float = float(last_close_value)
            # Se la conversione riesce, formatta e restituisci
            return f"Ultimo prezzo Close per l'oro: {price_as_float:.2f}"
        except (ValueError, TypeError):
            # Se la conversione fallisce, restituisci un errore chiaro
            return f"Errore: Il valore ricevuto da yfinance non è un numero ({last_close_value})."

    except Exception as e:
        # Questo cattura tutti gli altri errori imprevisti (es. problemi di rete)
        return f"Errore generico in yfinance: {e}"

def analyze_market():
    return get_market_data()
