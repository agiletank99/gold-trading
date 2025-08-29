# main_bot.py (Fase 1: Logica e Comandi)
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Importiamo i moduli ora necessari
import analysis
import risk_management # RIATTIVATO

# Leggi le variabili d'ambiente
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Parametri globali (Rischio e Capitale)
CAPITALE_INIZIALE_DEMO = 10000.0
RISK_PER_TRADE_PERCENT = 1.5 # MAX 1.5% di rischio
RR_RATIO = 2.0

# Configura logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Stato del Bot (Aggiornato per supportare posizioni complete)
bot_state = {
    "is_running": False,
    "mode": "DEMO",
    "balance": CAPITALE_INIZIALE_DEMO,
    "open_positions": [], # useremo solo un trade alla volta per ora
    "closed_trades": []
}

# --- FUNZIONI COMANDI ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_state["is_running"] = True
    chat_id = update.effective_chat.id
    
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs: job.schedule_removal()

    # Aggiungiamo il job di analisi oraria
    context.job_queue.run_repeating(market_analysis_job, interval=3600, first=10, name=str(chat_id), chat_id=chat_id)
    
    await update.message.reply_text('✅ **AI Trading Bot AVVIATO**\nAnalisi oraria attivata. Modalità: DEMO.', parse_mode='Markdown')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_state["is_running"] = False
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs: job.schedule_removal()
    await update.message.reply_text('🛑 **AI Trading Bot FERMATO**.', parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mode = bot_state["mode"]
    balance = bot_state["balance"]
    
    positions = "Nessuna posizione aperta."
    if bot_state["open_positions"]:
        p = bot_state["open_positions"][0]
        positions = f"1️⃣ **{p['direction']} XAU/USD**\n   Entry: ${p['entry_price']}\n   SL: ${p['stop_loss']} | TP: ${p['take_profit']}"

    status_msg = f"""
