import vk_api
import data

def main():
    vk_session = vk_api.VkApi(data.login, data.password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)
    wall = tools.get_all('wall.get', 1, {'owner_id': -data.public_id})

    print(wall['items'][1]['date'])


if __name__ == '__main__':
    main()