import json


def for_admin(func):
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

    def f(update, context):
        if update.message.chat_id == data['admin_chat']:
            return func(update, context)
    return f
