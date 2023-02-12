import telebot

from DataClass import Data


class TGBridge:
    def __init__(self, data: Data) -> None:
        self.bot = telebot.TeleBot(data.tg_token)
        self.data = data
        self.init_commands()

    def init_commands(self):
        @self.bot.message_handler(commands=["start"])
        def start(message):
            chat_id = message.chat.id
            if chat_id not in self.data.chats:
                self.data.chats.append(chat_id)
                self.data.safe()
                self.send_message(chat_id, 'окей, буду держать вкурсе')
            else:
                self.send_message(chat_id, 'ты уже подписан на рассылку')

    def send_message(self, chat_id: int, message: str) -> None:
        self.bot.send_message(chat_id, message)

    def send_messages_to_chats(self, chats_id: list, messages: list) -> None:
        print(chats_id, list(map(str, messages)))
        for message in messages:
            for chat_id in chats_id:
                self.send_message(chat_id, message)

    def pull_once(self): pass
