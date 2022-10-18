import decorators
from bace_functions import *


def start(update, context):
    data = get_data()
    if update.message.chat_id not in data['chats']:
        data['chats'].append(update.message.chat_id)
        safe_data(data)
        context.bot.send_message(
            chat_id=update.message.chat_id, text='окей, буду держать вкурсе')
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id, text='ты уже подписан на рассылку')


@decorators.for_admin
def echo(update, context):
    data = json.loads(update.message.text[6:])
    safe_data(data)
    context.bot.send_message(chat_id=update.message.chat_id, text='ок')
