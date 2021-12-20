import json
import tg


def handler(event, context):
    event_body = json.loads(event['body'])

    chat = event_body['message']['chat']['id']

    file_id = get_file_id(event_body['message'])
    if not file_id:
        status, body = tg.send_message(chat=chat, text='send me a text file')
        assert status == 200, f"failed to send message: {body['description']}"

        return


    status, body = tg.get_file(file_id)
    if status != 200:
        status, _ = tg.send_message(chat=chat, text=body['description'])
        assert status == 200, f"failed to send message: {body['description']}"

        return


    file_path = body['result']['file_path']
    status, data = tg.download_file(file_path)
    if status != 200:
        status, _ = tg.send_message(chat=chat, text="failed to download file")
        assert status == 200, f"failed to send message: {body['description']}"

        return


    status, body = tg.send_message(chat=chat, text=data, parse_mode="MarkdownV2")

    if status != 200:
        status, _ = tg.send_message(chat=chat, text=body['description'])
        assert status == 200, f"failed to report error: {body['description']}"


def get_file_id(message):
    if 'document' in message:
        return message['document']['file_id']
