from flask import Flask, request, Response
from slackclient import SlackClient
import json
import os
import markovify


SLACK_APP_VERIFICATION_TOKEN = os.environ.get('SLACK_APP_VERIFICATION_TOKEN', '')
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN', '')


slack_client = SlackClient(SLACK_API_TOKEN)

# Read json corpus from file
with open('data.txt', 'r') as data_file:
    corpus = json.load(data_file)
reconstituted_model = markovify.Text.from_json(corpus)


app = Flask(__name__)


def send_message(channel_id, message):
    slack_client.api_call(
                          'chat.postMessage',
                          channel=channel_id,
                          text=message,
                          username='Overheard Bot',
                          icon_emoji=':speech_balloon:'
    )


@app.route('/', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_APP_VERIFICATION_TOKEN:
        channel_id = request.form.get('channel_id')
        message = reconstituted_model.make_short_sentence(140)
        send_message(channel_id, message)
        return Response(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
