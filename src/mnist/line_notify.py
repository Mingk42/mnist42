import os
import requests

def send(msg=None):
    headers = {
            'Authorization': 'Bearer ' + os.getenv('LINE_TOKEN', ''),
    }

    files = {
        'message': (None, msg),
    }

    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)