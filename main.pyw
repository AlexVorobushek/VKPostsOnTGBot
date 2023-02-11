from telegram.ext import Updater, CommandHandler
import telegram

import vk_api
import time
import datetime

from commands import start
from bace_functions import get_data, safe_data

with open('config.txt', 'r') as f:
    vk_login, vk_passwd, tg_token = f.read().split()

updater = Updater(tg_token)
dispatcher = updater.dispatcher
job_queue = updater.job_queue


token = vk_api.VkApi(
    token="056f6ab4056f6ab4056f6ab472067e655a0056f056f6ab46625d1a9ab53a8d836d5db0b")
vk = token.get_api()
tools = vk_api.VkTools(vk)

data = get_data()


def get_new_posts(public_id):
    posts = tools.get_all('wall.get', 5, {'owner_id': public_id})['items']
    posts = list(filter(lambda x: x['date'] > data['last_date'], posts))[::-1]
    return posts


def send_to_admin(context, text: str):
    context.bot.send_message(data['admin_chat'], text)


def send_post_to_chat(context, post, chat_id):
    try:
        context.bot.send_message(chat_id, f"from: {post['from_id']}\n{datetime.datetime.utcfromtimestamp(post['date'])}\n\n{post['text']}")
    except telegram.error.Unauthorized:
        data['chats'].remove(chat_id)
        send_to_admin(context, f"bot was blocked by the {chat_id} chat")


def run(context):
    global data
    print("in run")

    for public in data['publics']:
        posts = get_new_posts(public)
        for post in posts:
            for chat_id in data['chats']:
                send_post_to_chat(context, post, chat_id)
    
    print("for constr ended")
    data['last_date'] = int(time.time())
    safe_data(data)
    print('safed')
    # send_to_admin(context, time.time() - time_start)


dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(CommandHandler("echo", echo))
job_minute = job_queue.run_repeating(run, interval=60*3)

print('srarting polling')
updater.start_polling()
updater.idle()
