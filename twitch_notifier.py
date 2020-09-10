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
        self.stream_title = ''
        self.discord_url = ''
        self.discord_message = ''
        self.discord_description = ''
        self.streamer_data = dict()

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
    def check(self):
        while len(self.streamer_data['data']) < 1:
            self.authenticate()
            headers = {
                'Client-ID': self.client_id,
                'Authorization': 'Bearer ' + self.app_token['access_token'],
            }
            params = {'user_login': self.streamer.lower()}
            response = requests.get(self.twitch_api_url, headers=headers, params=params)

            self.streamer_data = response.json()




"""if __name__ == '__main__':
    bot = TwitchNotifier()
    bot.check()"""


