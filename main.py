from email import message
from telegram.ext import Updater, CommandHandler
import telegram

import vk_api
import json

from commands import *

with open('config.txt', 'r') as f:
    vk_login, vk_passwd, tg_token = f.read().split()

updater = Updater(tg_token)
dispatcher = updater.dispatcher
job_queue = updater.job_queue


vk_session = vk_api.VkApi(vk_login, vk_passwd)
vk_session.auth(token_only=True)
tools = vk_api.VkTools(vk_session)

data = get_data()

def get_new_posts(public_id):
    posts = tools.get_all('wall.get', 5, {'owner_id': public_id})['items']
    posts = list(filter(lambda x: x['date'] > data['last_date'], posts))[::-1]
    return posts

def run(context):
    global data
    data = get_data()
    posts = get_new_posts(data["public"])
    for post in posts:
        for chat in data['chats']:
            try:
                context.bot.send_message(chat, post['text'])
            except telegram.error.Unauthorized:
                data['chats'].remove(chat)
                context.bot.send_message(
                    data['admin_chat'], f"bot was blocked by the {chat} chat")
        data['last_date'] = post['date']
    safe_data(data)


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("echo", echo))
job_minute = job_queue.run_repeating(run, interval=10)

print('started')
updater.start_polling()
updater.idle()
