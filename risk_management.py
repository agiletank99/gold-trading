# risk_management.py
# Nota: Non abbiamo più pandas-ta, quindi usiamo ATR teorico per calcolo

def calculate_sl_tp(entry_price, direction, atr, rr_ratio):
    """Calcola Stop Loss e Take Profit basandosi sull'ATR."""
    # Usiamo 1.5 volte l'ATR per lo Stop Loss
    sl_multiplier = 1.5 * atr

    if direction.upper() == 'LONG':
        stop_loss = entry_price - sl_multiplier
        # Calcoliamo il Take Profit basato sul rapporto R/R
        take_profit = entry_price + (sl_multiplier * rr_ratio)
    elif direction.upper() == 'SHORT':
        stop_loss = entry_price + sl_multiplier
        take_profit = entry_price - (sl_multiplier * rr_ratio)
    else:
        return None, None
        
    return round(stop_loss, 2), round(take_profit, 2)

def calculate_position_size(balance, risk_percent, entry_price, stop_loss_price):
    """Calcola la dimensione della posizione in base al rischio."""
    capital_at_risk = balance * (risk_percent / 100)
    risk_per_unit = abs(entry_price - stop_loss_price)
    
    if risk_per_unit == 0:
        return 0
        
    position_size = capital_at_risk / risk_per_unit
    return round(position_size, 4)
