# RelayAdvisor (v1.0)

RelayAdvisorは、Slackチャンネル上でのリレー投稿（次の人の指名）を支援するBotアプリです。

Botをメンションして投稿すると、チャンネルのメンバー（投稿者以外）からランダムに1人を選んで提案の返信を行います。

## Installation

- https://api.slack.com/apps?new_granular_bot_app=1 でアプリを作成し、適切に設定。作成したBotを目的のチャンネルに追加しておく。

- 本スクリプト`relayadvisor.py`と同じディレクトリに`slack_token`という名前のファイルを置き、その1行目にBot Tokenを書き込む。

あとは Python3 (>= 3.6) で実行するだけです。SlackにアクセスできればグローバルIPは不要です。  
（クラッシュに備え、自動で再起動するよう設定することなどをお勧めします。）

