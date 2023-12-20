from telegram import Update, ForceReply
from telegram.ext import ContextTypes, CallbackContext

from transformers import pipeline


async def answer(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text("Please wait for the answer...")
        selected_model = context.user_data.get('selected_model', "microsoft/DialoGPT-medium")
        chatbot = pipeline("text-generation", model=selected_model)

        response = chatbot(f'''{update.message.text}''', max_length=500)
        await update.message.reply_text(fr'''Model: {selected_model}
Prompt: {update.message.text}
--------------------------------------
{response[0]['generated_text'].strip()}''')
    except Exception as e:
        await update.message.reply_text(f"Error:\n{e}")
