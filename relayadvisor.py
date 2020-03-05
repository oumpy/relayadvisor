# -*- coding: utf-8 -*-
from random import randrange
from datetime import datetime
from slack import WebClient, RTMClient
import os

base_dir = os.environ['HOME'] + '/var/relayadvisor/'
token_file = 'slack_token'

mute_keywords = ['(mute)', 'こっそり']

reply_message_format = '''\
あら、<@%s> さん、次の指名にお困りですか？
それなら、たとえば
```<@%s> さん```
に書いていただくのは、いかが？'''


token_file_path = base_dir + token_file

def next_writer(members):
    members = list(members)
    N = len(members)
    return members[randrange(N)]

def generate_reply_message(user_id, target_id):
    return reply_message_format % (user_id, target_id)


@RTMClient.run_on(event='message')
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
    members.discard(my_id)
    if len(members) > 1:
        members.discard(user)
    reply_message = generate_reply_message(user, next_writer(members))

    reply_broadcast = 'False'
#    for mkw in mute_keywords:
#        if mkw in text:
#            reply_broadcast = 'False'
#            break

    web_client.api_call(
        'chat.postMessage',
        params={
            'channel': channel_id,
            'text': reply_message,
            'thread_ts': thread_ts,
            'reply_broadcast': reply_broadcast,
        }
    )


if __name__ == '__main__':
    with open(token_file_path, 'r') as f:
        slack_token = f.readline().rstrip()
    web_client = WebClient(token=slack_token)
    my_id = web_client.api_call('auth.test')['user_id']

    rtm_client = RTMClient(token=slack_token)
    print('Running...')
    rtm_client.start()
