"""
author          : nsuhara <na010210dv@gmail.com>
date created    : 2019/5/1
python version  : 3.7.3
"""
import os
import sys
from argparse import ArgumentParser

from flask import Flask, abort, render_template, request
from jinja2 import FileSystemLoader
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage

from app.framework.nslinebot.controllers.handler import (MessageHandler,  # pylint: disable=E0611
                                                         PostbackHandler)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.jinja_loader = FileSystemLoader('app/liff')

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    sys.exit(1)
if channel_access_token is None:
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)  # pylint: disable=E1101
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK', 200


@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    MessageHandler(line_bot_api, event).handle_event()


@handler.add(PostbackEvent)
def on_postback(event):
    MessageHandler(line_bot_api, event).handle_event()


@app.route('/liff/<model>', methods=['GET'])
def liff(model=None):
    if model is None:
        return 'OK', 200
    return render_template('{}.html'.format(model)), 200


@app.route('/postback', methods=['POST'])
def postback():
    try:
        return PostbackHandler(request.get_data(as_text=True)).handle_event(), 200
    except Exception:
        abort(400)


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=True)
