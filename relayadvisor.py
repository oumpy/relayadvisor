# coding: utf-8
import sys
import random
from datetime import datetime
import slack
from slack import WebClient, RTMClient

token_file = './slack_token'

mute_keywords = ['(mute)', 'こっそり']

def get_channel_list(client):
    channels = client.api_call('channels.list')
    if channels['ok']:
        return channels['channels']
    else:
        return None

def get_channel_id(client, channel_name):
    channels = filter(lambda x: x['name']==channel_name , get_channel_list(client))
    target = None
    for c in channels:
        if target is not None:
            break
        else:
            target = c
    if target is None:
        return None
    else:
        return target['id']

def next_writer(members):
    members = list(members)
    N = len(members)
    return members[random.randrange(N)]

def generate_reply_message(user_id, target_id):
    message = f'あら、<@{user_id}> さん、'
    message += '次の指名にお困りですか？\n'
    message += 'それなら、たとえば\n'
    message += f'```<@{target_id}> さん```\n'
    message += 'に書いていただくのは、いかが？'
    return message

@RTMClient.run_on(event="message")
def write_advice(**payload):
    print(f'Message received at {str(datetime.now())}.')

    data = payload['data']
    web_client = payload['web_client']
    required_fields = ['text', 'channel', 'ts', 'user']
    for f in required_fields:
        if f not in data.keys():
            return
    channel_id = data['channel']
    text = data['text']
    thread_ts = data['ts']
    user = data['user']

    # respond only to mentions to me in target channel.
    if not f'<@{my_id}>' in text:
        return

    channel_info = web_client.api_call('channels.info', params={'channel':channel_id})['channel']
    # ensure I am a member of the channel.
    if not channel_info['is_member']:
        return

    members = set(channel_info['members'])
    members.remove(my_id)
    if len(members) > 1:
        members.remove(user)
    reply_message = generate_reply_message(user, next_writer(members))

    reply_broadcast = 'True'
    for mkw in mute_keywords:
        if mkw in text:
            reply_broadcast = 'False'
            break

    web_client.api_call(
        'chat.postMessage',
        params={
            'channel': channel_id,
            'text': reply_message,
            'thread_ts': thread_ts,
            'reply_broadcast': reply_broadcast
            }
    )


if __name__ == "__main__":
    with open(token_file, 'r') as f:
        slack_token = f.readline()
    web_client = WebClient(token=slack_token)
    my_id = web_client.api_call('auth.test')['user_id']

    rtm_client = RTMClient(token=slack_token)
    print('Running...')
    rtm_client.start()
