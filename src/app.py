import tg
import json


def handler(event, context):
    event_body = json.loads(event['body'])
    chat = event_body['message']['chat']['id']
    text = event_body['message']['text']

    status, body = tg.send_message(chat=chat, text=text, parse_mode="Markdown")

    if status != 200:
        status, _ = tg.send_message(chat=chat, text=body['description'])
        assert status == 200, f"failed to report error: {body['description']}"
