from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf'''Hi {user.mention_html()}!

Use /help command to see what you can do.''',
        reply_markup=ForceReply(selective=True),
    )


async def model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(text="gpt2", callback_data='gpt2'),
        InlineKeyboardButton(text="distilgpt2", callback_data='distilgpt2'),
        InlineKeyboardButton(text="flan-t5-base", callback_data='google/flan-t5-base'),
        InlineKeyboardButton(text="DialoGPT-m", callback_data='microsoft/DialoGPT-medium')
    ]])

    await update.message.reply_text("Choose model.", reply_markup=markup)


async def button(update, context):
    data = update.callback_query.data

    context.user_data['selected_model'] = data

    await update.callback_query.answer(text=f"You chose model: {data}")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        rf'''/start command shows 'hello' message.
/model command to choose AI model.

Use text without '/' symbol at start to talk to the bot.''',
        reply_markup=ForceReply(selective=True),
    )
