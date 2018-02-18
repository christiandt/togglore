import urllib
import requests
import base64
import json


class TogglClient(object):
    def __init__(self, api_token, user_id, workspace):
        self.api_token = api_token
        self.user_id = user_id
        self.workspace = workspace
        self.headers = {}
        self.__init_headers()

    def __init_headers(self):
        auth_header = self.api_token + ":" + "api_token"
        auth_header = "Basic {}".format(base64.b64encode(bytes(auth_header).decode("ascii")))
        self.headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "togglore",
        }

    def request(self, endpoint, parameters=None):
        if parameters is not None:
            url = '{}?{}'.format(endpoint, urllib.urlencode(parameters))
        else:
            url = endpoint

        response = requests.get(url, headers=self.headers)
        return json.loads(response.text)

    def time_entries(self, date_range):
        entries = []

        total = 1
        per_page = 0
        current_page = 0

        while current_page * per_page < total:
            current_page += 1
            response = self.request(
                'https://toggl.com/reports/api/v2/details?workspace_id={}&since={}&until={}&user_agent=togglore&page={}'.format(
                    self.workspace, date_range.start.isoformat(), date_range.end.isoformat(), current_page))
            total = response['total_count']
            per_page = response['per_page']
            for time in response['data']:
                if str(time['uid']) == self.user_id:
                    entries.append(time)

        return entries

