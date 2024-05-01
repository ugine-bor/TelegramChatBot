from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class ChatBot:
    def __init__(self, model, tokenizer, pipeline, history, settings, structure, need_tokenizer=False):
        self._model = model
        self._tokenizer = tokenizer
        self._pipeline = pipeline
        self._history = history if history is not None else []
        self._settings = settings
        self._structure = structure

        self.need_tokenizer = need_tokenizer

    def send_message(self, message):
        conversation = ''.join(self.history)
        structure = self._structure

        print('Send message: \n',
              f"{conversation}{structure['newline']}{structure['open']}{structure['user_tag']}{structure['close']}{structure['newline']}{message}{structure['open']}{structure['close_tag']}{structure['close']}{structure['newline']}{structure['open']}{structure['assistant_tag']}{structure['close']}{structure['newline']}",
              '\n')

        response = self.pipeline(
            f"{conversation}{structure['newline']}{structure['open']}{structure['user_tag']}{structure['close']}{structure['newline']}{message}{structure['open']}{structure['close_tag']}{structure['close']}{structure['newline']}{structure['open']}{structure['assistant_tag']}{structure['close']}{structure['newline']}",
            **self.settings)

        self._history.append(
            f"{structure['open']}{structure['user_tag']}{structure['close']}{structure['newline']}{message}{structure['open']}{structure['close_tag']}{structure['close']}{structure['newline']}{structure['open']}{structure['assistant_tag']}{structure['close']}{structure['newline']}")

        return response

    @classmethod
    def set_settings(cls, settings):
        cls._settings = settings

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, **value):
        self._model = value

    @model.getter
    def model(self):
        return self._model

    @property
    def tokenizer(self):
        return self._tokenizer

    @tokenizer.setter
    def tokenizer(self, **value):
        self._tokenizer = value

    @tokenizer.getter
    def tokenizer(self):
        return self._tokenizer

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, **value):
        self._pipeline = value

    @pipeline.getter
    def pipeline(self):
        return self._pipeline

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, **value):
        self._settings = value

    @settings.getter
    def settings(self):
        return self._settings

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    @history.getter
    def history(self):
        return self._history

    def __str__(self):
        return type(self.model).__name__


def set_model(model):
    if model == "gpt2":
        history = ['']
        selected_model = AutoModelForCausalLM.from_pretrained(
            "gpt2",
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        pipe = pipeline(
            "text-generation",
            model=selected_model,
            tokenizer=tokenizer,
        )
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "do_sample": False,
        }
        structure = {'open': '', 'close': '', 'system_tag': '', 'close_tag': '',
                     'assistant_tag': '', 'user_tag': '', 'newline': ''}
    elif model == "microsoft/Phi-3-mini-4k-instruct":
        history = ['''<|system|>
        You are a helpful AI assistant.<|end|>
        ''']
        selected_model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        pipe = pipeline(
            "text-generation",
            model=selected_model,
            tokenizer=tokenizer,
        )
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "do_sample": False,
        }
        structure = {'open': '<|', 'close': '|>', 'system_tag': 'system', 'close_tag': 'end',
                     'assistant_tag': 'assistant', 'user_tag': 'user', 'newline': '\n'}
    elif model == "microsoft/Phi-3-mini-128k-instruct":
        history = ['''<|system|>
        You are a helpful AI assistant.<|end|>
        ''']
        selected_model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-128k-instruct",
            device_map="cuda",
            torch_dtype="auto",
            trust_remote_code=True,
            attn_implementation='eager'
        )
        tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")
        pipe = pipeline(
            "text-generation",
            model=selected_model,
            tokenizer=tokenizer,
        )
        generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            "do_sample": False,
        }
        structure = {'open': '<|', 'close': '|>', 'system_tag': 'system', 'close_tag': 'end',
                     'assistant_tag': 'assistant', 'user_tag': 'user', 'newline': '\n'}
    else:
        return None

    return ChatBot(model=selected_model, tokenizer=tokenizer, pipeline=pipe, history=history,
                   settings=generation_args, structure=structure)


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
        InlineKeyboardButton(text="Phi-3-mini-4k", callback_data='microsoft/Phi-3-mini-4k-instruct'),
        InlineKeyboardButton(text="Phi-3-mini-128k", callback_data='microsoft/Phi-3-mini-128k-instruct')
    ]])

    await update.message.reply_text("Choose model.", reply_markup=markup)


async def button(update, context):
    model = update.callback_query.data

    bot = set_model(model)
    context.user_data['bot'] = bot

    await update.callback_query.answer(text=f"You chose model: {str(bot)}")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        rf'''/start command shows 'hello' message.
/model command to choose AI model.

Use text without '/' symbol at start to talk to the bot.''',
        reply_markup=ForceReply(selective=True),
    )
