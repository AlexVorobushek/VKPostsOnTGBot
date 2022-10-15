import telebot
import time
import json

with open('data.json', 'r') as f:
    data = json.loads(f.read())

def get_posts():
    import vk_api

    vk_session = vk_api.VkApi(data['login'], data['password'])

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)
    posts = list(
        filter(
            lambda x: x['date'] > data['date'],
            tools.get_all(
                'wall.get',
                1,
                {'owner_id': -data['public_id']}
            )['items']
        )
    )
    return posts[::-1]

def safe_data():
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

bot = telebot.TeleBot(data['bot_token'])
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     data['chats'] = set(data['chats'])
#     data['chats'].add(message.chat.id)
#     data['chats'] = list(data['chats'])
#     safe_data()
#     bot.send_message(message.chat.id, "ок, буду держать в курсе")
# bot.polling()

while True:
    posts = get_posts()
    for post in posts:
        for chat in data['chats']:
            bot.send_message(chat, post['text'])
        data['date'] = post['date']
        safe_data()
    # time.sleep(123)
