import requests
import json
from time import sleep


class TwitchNotifier:
    """Initializing Class"""
    def __init__(self):
        with open("Config/config.json") as f:
            configs = json.load(f)

        self.client_id = configs['client_id']
        self.secret_key = configs['client_secret']
        self.app_token = dict()
        self.streamer = configs['streamer']
        self.twitch_api_url = configs['twitch_api_url']
        self.stream_url = configs['stream_url']
        self.discord_url = configs['discord_url']
        self.discord_message = configs['discord_message']
        self.discord_description = ''
        self.streamer_data = {"data": []}
        self.game_name = ''

    """Authenticating for app token"""
    def authenticate(self):
        token_params = {
            'client_id': self.client_id,
            'client_secret': self.secret_key,
            'grant_type': 'client_credentials',
        }
        app_token_request = requests.post('https://id.twitch.tv/oauth2/token', params=token_params)
        self.app_token = app_token_request.json()

    """Check for the streamer is live or not"""
    def is_he_live(self):
        self.authenticate()
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.app_token['access_token'],
        }
        params = {'user_login': self.streamer.lower()}
        response = requests.get(self.twitch_api_url, headers=headers, params=params)

        try:
            if len(response.json()['data']) >= 1:
                self.streamer_data = response.json()
                print("Stream is live!!!")

                try:
                    game_name_search_url = "https://api.twitch.tv/helix/games"
                    game_params = {'id': self.streamer_data['data'][0]['game_id']}
                    game_json = requests.get(game_name_search_url, headers=headers, params=game_params).json()
                    self.game_name = game_json['data'][0]['name']
                except ValueError as v:
                    pass

                """This is to collect user information"""
                """user_search_url = "https://api.twitch.tv/helix/users"
                user_params = {'login': self.streamer.lower()}
                user_data_json = requests.get(user_search_url, headers=headers, params=user_params).json()"""

                return True
            else:
                print("Not Online Yet!!!")
        except ValueError as v:
            print(v)
            return False

    """Sent message to discord"""
    def notify_discord(self):
        if len(self.game_name) > 0:
            self.discord_description = f"Game: {self.game_name}"
        self.discord_message += f"\n{self.stream_url}"
        discord_payload = {
            "content":  self.discord_message,
            "embeds": [
                {
                    "title": self.streamer_data['data'][0]['title'],
                    "url": self.stream_url,
                    "description": self.discord_description
                }
            ]
        }

        status_code = 0
        while status_code != 204:
            discord_request = requests.post(self.discord_url, json=discord_payload)
            status_code = discord_request.status_code

            if discord_request.status_code == 204:
                print("Successfully called Discord API. Waiting 5 seconds to terminate...")
                sleep(5)
            else:
                print("Failed to call Discord API. Waiting 5 seconds to retry...")
                sleep(5)


if __name__ == '__main__':
    bot = TwitchNotifier()
    if bot.is_he_live():
        bot.notify_discord()


