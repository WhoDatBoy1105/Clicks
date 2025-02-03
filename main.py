import requests
import os
import sys
import argparse
from dotenv import load_dotenv


API_VERSION = '5.131'


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_input_url', nargs='?')
    parser.add_argument('--debug', action='store_true', help="Enable debug mode to show raw API responses.")
    return parser


def is_vk_short_link(url):
    return url.startswith("https://vk.cc/") or url.startswith("http://vk.cc/")


def is_short_link(url, access_token, api_version, debug=False):
    response = requests.get(
        'https://api.vk.com/method/utils.checkLink',
        params={
            'url': url,
            'access_token': access_token,
            'v': api_version
        }
    )
    response.raise_for_status()

    response_data = response.json()
    if debug:
        print("Response from utils.checkLink:", response_data)  # Логирование только в режиме отладки
    if 'error' in response_data:
        raise Exception(f"Error: {response_data['error']['error_msg']}")
    return response_data['response']['status'] == 'not_banned'


def count_clicks(shortened_url, access_token, api_version, debug=False):
    response = requests.get(
        'https://api.vk.com/method/utils.getLinkStats',
        params={
            'key': shortened_url.split('/')[-1],
            'access_token': access_token,
            'v': api_version
        }
    )
    response.raise_for_status()

    response_data = response.json()
    if debug:
        print("Response from utils.getLinkStats:", response_data)  # Логирование только в режиме отладки
    if 'error' in response_data:
        raise Exception(f"Error: {response_data['error']['error_msg']}")

    stats = response_data['response']['stats']
    total_clicks = sum(stat['views'] for stat in stats)

    return total_clicks


def shorten_link(original_url, access_token, api_version, debug=False):
    response = requests.get(
        'https://api.vk.com/method/utils.getShortLink',
        params={
            'url': original_url,
            'access_token': access_token,
            'v': api_version
        }
    )
    response.raise_for_status()

    response_data = response.json()
    if debug:
        print("Response from utils.getShortLink:", response_data)
    if 'error' in response_data:
        raise Exception(f"Error: {response_data['error']['error_msg']}")

    return response_data['response']['short_url']


def main():
    load_dotenv()
    try:
        vk_access_token = os.environ['VK_ACCESS_TOKEN']
    except KeyError:
        sys.exit("Ошибка: Укажите переменную окружения VK_ACCESS_TOKEN.")

    parser = createParser()
    args = parser.parse_args()

    user_input_url = args.user_input_url
    debug_mode = args.debug

    if not user_input_url:
        sys.exit("Ошибка: Укажите ссылку в качестве аргумента.")

    try:
        if is_vk_short_link(user_input_url):
            print(user_input_url)
            clicks = count_clicks(user_input_url, vk_access_token, API_VERSION, debug=debug_mode)
            print(f"По вашей ссылке перешли {clicks} раз")
        else:
            if is_short_link(user_input_url, vk_access_token, API_VERSION, debug=debug_mode):
                shortened_url = shorten_link(user_input_url, vk_access_token, API_VERSION, debug=debug_mode)
                print(shortened_url)
            else:
                print("Ссылка не может быть обработана.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
    except Exception as err:
        print(f"Ошибка: {err}")


if __name__ == '__main__':
    main()
