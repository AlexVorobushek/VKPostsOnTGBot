from telegram.ext import Updater, CommandHandler
import telegram

import vk_api
import json

vk_data = {'login': input(), 'password': input()}
tg_data = {'token': input()}

updater = Updater(tg_data['token'])
dispatcher = updater.dispatcher
job_queue = updater.job_queue


vk_session = vk_api.VkApi(vk_data['login'], vk_data['password'])
vk_session.auth(token_only=True)
tools = vk_api.VkTools(vk_session)

with open('data.json', 'r') as f:
    data = json.loads(f.read())


def start(update, context):
    if update.message.chat_id not in data['chats']:
        data['chats'].append(update.message.chat_id)
        context.bot.send_message(chat_id=update.message.chat_id, text='окей, буду держать вкурсе')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='ты уже подписан на рассылку')

def _load_data(update, context):
    global data
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

def get_new_posts(public_id):
    posts = tools.get_all('wall.get', 5, {'owner_id': public_id})['items']
    posts = list(filter(lambda x: x['date'] > data['last_date'], posts))[::-1]
    return posts

def safe_data():
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

def run(context):
    posts = get_new_posts(data["public"])
    print(len(posts))
    for post in posts:
        for chat in data['chats']:
            try:
                context.bot.send_message(chat, post['text'])
            except telegram.error.Unauthorized:
                data['chats'].remove(chat)
                context.bot.send_message(data['admin_chat'], f"bot was blocked by the {chat} chat")
        data['last_date'] = post['date']
        safe_data()


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("load_data", _load_data))
job_minute = job_queue.run_repeating(run, interval=10)

print('started')
updater.start_polling()
updater.idle()
