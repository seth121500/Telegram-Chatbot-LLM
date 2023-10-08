import os
import websocket
#from Vox import speak
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, ApplicationBuilder, MessageHandler, ApplicationHandlerStop, ContextTypes, TypeHandler, filters
from Coraline_model import run, history_append
from Vox import speak
from Coraline_Voice_JP import translate_text
import requests
import datetime
from dotenv import load_dotenv
import asyncio

from bs4 import BeautifulSoup
import base64
import io

load_dotenv()
CREATOR_ID = os.getenv('CREATOR_ID')
if CREATOR_ID is not None:
    CREATOR_ID = int(CREATOR_ID)
Telegram_API  = os.getenv('TELEGRAM_API')

async def send_message(update: Update, Coraline_Text):
    Coraline_JP = translate_text(Coraline_Text)
    speak(Coraline_JP)
    audio_JP = 'output.wav'
    performer = "Coraline"  # Replace with your bot's name
    title = " "

    sentence_delimiters = ['.', '!', '?']

    sentences = []

    current_sentence = ''
    for char in Coraline_Text:
        current_sentence += char
        if char in sentence_delimiters:
            sentences.append(current_sentence.strip())
            current_sentence = ''

    for sentence in sentences:
        if sentence:
            await update.message.reply_text(sentence)
    


    output_text = "output.txt"

    with open(output_text, 'w', encoding='utf-8') as text:
        text.write(Coraline_JP)

    await update.message.reply_audio(audio=open(audio_JP, 'rb'))




async def whitelist_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CREATOR_ID:
        await update.effective_message.reply_text("Nope.")
        raise ApplicationHandlerStop

#async def whitelist_mentions(update: Update, context: ContextTypes.DEFAULT_TYPE):

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = ['/start', '/stop', '/cancel']
    user_states = context.user_states
    sender = update.message.from_user

    if update.message.text in commands:
        if update.message.text == '/start':
            await start_command(update, context)
        elif update.message.text == '/stop':
            await stop_command(update, context)
        elif update.message.text == '/cancel':
            await cancel_command(update, context)
    else:
        await update.message.reply_text("I don't understand that command.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the bot! This is the /start command.")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot stopped. You can restart it with /start.")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")




async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_states = context.user_states
    sender = update.message.from_user

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%I:%M %p')

    with open('Context.txt', 'r') as file:
        context = file.read()

    context_with_current_time = context.replace('<Time>', formatted_time)


    Coraline_Text = run(update.message.text,context_with_current_time)


    img_tags = BeautifulSoup(Coraline_Text, "html.parser").find_all('img')

    if img_tags:
        img_tag = img_tags[0]
        img_data_uri = img_tag['src']
        alt_text = img_tag['alt']

        if img_data_uri.startswith('data:image/jpeg;base64'):
            
            img_data = img_data_uri.split(',')[1]
            img_bytes = base64.b64decode(img_data)

            await update.message.reply_photo(photo=img_bytes, caption=alt_text)
            history_append(update.message.text, alt_text)
        else:
            await send_message(update, Coraline_Text)
            #await update.message.reply_text(Coraline_Text)
            history_append(update.message.text, Coraline_Text)
    else:
        await send_message(update, Coraline_Text)
        #await update.message.reply_text(Coraline_Text)
        history_append(update.message.text, Coraline_Text)


    #await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_JP, 'rb'))



def run_telegram():
    app = ApplicationBuilder().token(Telegram_API).build()

    filter_users = TypeHandler(Update, whitelist_users)
    app.add_handler(filter_users, -1)
    command_handler = MessageHandler(filters.COMMAND, handle_command)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    handlers = [command_handler, message_handler]
    for handler in handlers:
        app.add_handler(handler)

    user_states = {}
    app.context_types.context.user_states = user_states
    app.run_polling()
    
if __name__ == '__main__':
    run_telegram()
