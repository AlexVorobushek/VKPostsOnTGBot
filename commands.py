import decorators
import json


def start(update, context):
    if update.message.chat_id not in data['chats']:
        data['chats'].append(update.message.chat_id)
        context.bot.send_message(
            chat_id=update.message.chat_id, text='окей, буду держать вкурсе')
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id, text='ты уже подписан на рассылку')


@decorators.for_admin
def echo(update, context):
    global data
    text, file = json.loads(update.message.text[6:])
    with open(file, 'w') as f:
        f.write(text)
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    context.bot.send_message(chat_id=update.message.chat_id, text='ок')
