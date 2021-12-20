import json
import tg


def handler(event, context):
    event_body = json.loads(event['body'])

    chat = event_body['message']['chat']['id']

    if 'document' not in event_body['message']:
        return send_message(chat=chat, text='send me a plain text file')
    
    document = event_body['message']['document']
    if document['file_size'] > 10 * 1024:
        return send_message(chat=chat, text='file must be smaller than 10KB')

    status, body = tg.get_file(document['file_id'])
    if status != 200:
        return send_message(chat=chat, text=body['description'])

    file_path = body['result']['file_path']
    status, data = tg.download_file(file_path)
    if status != 200:
        return send_message(chat=chat, text="failed to download file")

    status, body = tg.send_message(chat=chat, text=data, parse_mode="MarkdownV2")
    if status != 200:
        return send_message(chat=chat, text=body['description'])


def send_message(chat, text):
    status, body = tg.send_message(chat=chat, text=text)
    assert status == 200, f"failed to send message: {body['description']}"
