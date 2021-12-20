import argparse
import requests
import json

argparser = argparse.ArgumentParser()
argparser.add_argument("--token", type=str, required=True)
argparser.add_argument("--url", type=str, required=True)
args = argparser.parse_args()


def set_webhook():
    url = f"https://api.telegram.org/bot{args.token}/setWebhook"
    resp = requests.post(url,
                         json={
                             'url': args.url,
                             'allowed_updates': json.dumps(["message"])
                         })

    assert resp.ok, f"FAILURE: (status: {resp.status_code}, details: {resp.json()['description']})"


if __name__ == "__main__":
    set_webhook()
