import json
import os
import requests
import time

from src.app import handler

TOKEN = os.environ["TOKEN"]


def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    resp = requests.post(url,
                         json={
                             "offset": offset,
                             "allowed_updates": json.dumps(["message"])
                         })

    assert resp.ok, f"get_updates failed: (status: {resp.status_code}; data: {resp.json()})"

    resp_body = resp.json()
    assert resp_body[
        'ok'], f"get_updates call failed: {resp_body['description']}"

    return resp_body['result']


def loop():
    offset = 0

    while True:
        updates = get_updates(offset)
        for update in updates:
            update_id = update['update_id']
            if update_id >= offset:
                offset = update_id + 1

            print(update)

            update = {'body': json.dumps(update)}

            handler(update, {})

        time.sleep(1)


if __name__ == "__main__":
    loop()
