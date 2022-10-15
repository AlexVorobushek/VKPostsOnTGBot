import telebot
import time
import json
import vk_api

with open('data.json', 'r') as f:
    data = json.loads(f.read())

vk_session = vk_api.VkApi(data['login'], data['password'])
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
    exit()

tools = vk_api.VkTools(vk_session)

def get_posts():
    posts = []
    for public_id in data['publics_id']:
        posts += tools.get_all('wall.get', 1, {'owner_id': public_id})['items']
    posts = list(filter(lambda x: x['date'] > data['date'], posts))[::-1]
    return posts

def safe_data():
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

bot = telebot.TeleBot(data['bot_token'])
while True:
    posts = get_posts()
    for post in posts:
        for chat in data['chats']:
            bot.send_message(chat, post['text'])
        data['date'] = post['date']
        safe_data()
    time.sleep(60)
