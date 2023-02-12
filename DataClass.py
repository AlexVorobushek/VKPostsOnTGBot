import os
import time
import json

DATA_FILE_PATH = 'data.json'
class Data:
    def __init__(self) -> None:
        self.vk_token = '056f6ab4056f6ab4056f6ab472067e655a0056f056f6ab46625d1a9ab53a8d836d5db0b'
        self.tg_token = '5432792381:AAEBxq4BNCe6xwToLSVS8sPFdlWth6sNQUw'
        self.publics = [-206763521, -194010932, 324086248]

        if os.path.exists(DATA_FILE_PATH):
            self.__load_data()
        else:
            self.last_time = time.time()
            self.chats = []
    
    def __load_data(self) -> None:
        with open(DATA_FILE_PATH) as file:
            readed_dict = json.loads(file.read())
            self.last_time = readed_dict['last_time']
            self.chats = readed_dict['chats']
    
    def safe(self) -> None:
        with open(DATA_FILE_PATH, 'w') as file:
            file.write(json.dumps(self.get_dict()))
    
    def get_dict(self) -> dict:
        return {
            'chats': self.chats,
            'last_time': self.last_time
        }
