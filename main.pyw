from commands import start
from DataClass import Data
from TGBridgeClass import TGBridge
from VKBridgeClass import VKBridge

data = Data()
tg_bridge = TGBridge(data)
vk_bridge = VKBridge(data.vk_token)


def main():
    global data

    while True:
        tg_bridge.pull_once()
        
        new_posts = []
        while not new_posts:
            for public_id in data.publics:
                new_posts += vk_bridge.get_new_posts(public_id, data.last_time)
        
        print(list(map(str, new_posts)))

        new_posts.sort(key=lambda post: post.date)
        tg_bridge.send_messages_to_chats(data.chats, new_posts)
        print('sended')

        data.last_time = int(new_posts[-1].time)
        data.safe()


if __name__ == "__main__":
    main()
