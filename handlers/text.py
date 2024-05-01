from telegram import Update
from telegram.ext import CallbackContext


async def answer(update: Update, context: CallbackContext):
    print(context.user_data)
    if context.user_data:
        bot = context.user_data['bot']
        await update.message.reply_text("Please wait for the answer...")

        response = bot.send_message(update.message.text)
        bot.history += response[0]['generated_text'].strip()

        await update.message.reply_text(fr'''Model: {bot}
    Prompt: {update.message.text}
    --------------------------------------
    {response[0]['generated_text'].strip()}''')
