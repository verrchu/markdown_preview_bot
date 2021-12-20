import os
import requests

TIMEOUT = 5
TOKEN = os.environ["TOKEN"]
URL = "https://api.telegram.org"


def send_message(text, chat, parse_mode=None):
    url = f"{URL}/bot{TOKEN}/sendMessage"

    req = {"chat_id": chat, "text": text}
    if parse_mode:
        req['parse_mode'] = parse_mode

    resp = requests.post(url, timeout=TIMEOUT, json=req)
    return resp.status_code, resp.json()


def get_file(file_id):
    url = f"{URL}/bot{TOKEN}/getFile"
    resp = requests.post(url, timeout=TIMEOUT, json={"file_id": file_id})
    return resp.status_code, resp.json()


def download_file(file_path):
    url = f"{URL}/file/bot{TOKEN}/{file_path}"
    resp = requests.get(url, timeout=TIMEOUT)
    return resp.status_code, resp.text
