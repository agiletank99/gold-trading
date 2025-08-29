# main_bot.py (Fase 1: Logica e Comandi - VERSIONE CORRETTA)
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import analysis
import risk_management

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

CAPITALE_INIZIALE_DEMO = 10000.0
RISK_PER_TRADE_PERCENT = 1.5
RR_RATIO = 2.0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot_state = {
    "is_running": False,
    "mode": "DEMO",
    "balance": CAPITALE_INIZIALE_DEMO,
    "open_positions": [],
    "closed_trades": []
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_state["is_running"] = True
    chat_id = update.effective_chat.id
    
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()

    context.job_queue.run_repeating(market_analysis_job, interval=3600, first=10, name=str(chat_id), chat_id=chat_id)
    
    await update.message.reply_text('✅ **AI Trading Bot AVVIATO**\nAnalisi oraria attivata. Modalità: DEMO.', parse_mode='Markdown')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_state["is_running"] = False
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()
    await update.message.reply_text('🛑 **AI Trading Bot FERMATO**.', parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT
