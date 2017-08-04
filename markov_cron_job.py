from slackclient import SlackClient
import json
import os
import markovify
import re


SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN', '')
CHANNEL_ID = 'C1AMF7UTU'

slack_client = SlackClient(SLACK_API_TOKEN)

has_more_messages = True
messages = []
latest_ts = ''

while has_more_messages:
    if len(latest_ts) == 0:
        channel_history = slack_client.api_call("channels.history", channel=CHANNEL_ID)
    else:
        channel_history = slack_client.api_call("channels.history", channel=CHANNEL_ID, latest=latest_ts)
    if channel_history['ok']:
        print len(channel_history['messages'])
        for message in channel_history['messages']:
            if message['text']:
                quote_text = re.findall('"([^"]*)"', message['text'])
                if len(quote_text) > 0:
                    text = " ".join(quote_text)
                    messages.append(text)
    if channel_history['has_more']:
        latest_ts = channel_history['messages'][-1]['ts']
    else:
        has_more_messages = False

combined_text = '\n'.join(messages)
text_model = markovify.NewlineText(combined_text)
model_json = text_model.to_json()
# Write new corpus to file
with open('data.txt', 'w') as outfile:
    json.dump(model_json, outfile)
