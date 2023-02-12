import vk_api

from PostClass import Post


class VKBridge:
    def __init__(self, token) -> None:
        self.token = vk_api.VkApi(token=token)
        self.vk = self.token.get_api()
        self.tools = vk_api.VkTools(self.vk)

    def get_new_posts(self, public_id: int, last_time: float) -> list:
        posts = self.tools.get_all(
            'wall.get', 5, {'owner_id': public_id})['items']
        posts = list(filter(lambda post: post['date'] > last_time, posts))[::-1]
        return [Post(post) for post in posts]
