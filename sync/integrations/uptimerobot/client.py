from typing import Union

import requests

from backups.settings import UPTIME_MONITOR_KEY as key


class UptimeRobot:
    HEADERS = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
    }

    def __init__(self, api_key: str = key) -> None:
        self.api_key: str = api_key
        self.url: str = "https://api.uptimerobot.com/v2/getMonitors"

    def get_monitors(self) -> Union[dict, str]:
        """Gets a list of all monitors available."""
        payload = f"api_key={self.api_key}&format=json"
        response = requests.post(self.url, data=payload, headers=self.HEADERS)
        return response.json() if response.ok else response.text
