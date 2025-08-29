import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import analysis

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("ERRORE: Variabile TELEGRAM_TOKEN non trovata!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def analysis_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Esecuzione analisi...")
    chat_id = context.job.chat_id
    risultato_analisi = analysis.analyze_market()
    await context.bot.send_message(chat_id, text=f"Report Orario:\n{risultato_analisi}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if not current_jobs:
        context.job_queue.run_repeating(analysis_job, interval=3600, first=10, name=str(chat_id), chat_id=chat_id)
        await update.message.reply_text("✅ Bot avviato! Analisi oraria attivata.")
    else:
        await update.message.reply_text("ℹ️ Bot già in esecuzione.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()
    await update.message.reply_text("🛑 Bot fermato. Analisi interrotta.")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.run_polling()

if __name__ == '__main__':
    main()