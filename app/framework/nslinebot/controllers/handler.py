"""
author          : nsuhara <na010210dv@gmail.com>
date created    : 2019/5/1
python version  : 3.7.3
"""
import json
import logging

from app.framework.nslinebot.views.messenger import Messenger
from app.models import MESSAGE_MODELS, MODELS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageHandler(object):
    def __init__(self, line_bot_api, event):
        self._GET_EVENT = {
            'message': self._get_message_event,
            'postback': self._get_postback_event
        }
        self.line_bot_api = line_bot_api
        self.event = event
        self.event_type = event.type

    def handle_event(self):
        logger.info('handle_event:{}'.format(self.event))
        event_data = self._GET_EVENT.get(self.event_type)()
        if event_data is None:
            return

        model = event_data.get('model')
        scene = event_data.get('scene')
        process = event_data.get('process', None)
        method = event_data.get('method', 'reply')
        model_instance = MODELS.get(model)()

        text = model_instance.process_handler(process) if process else None
        messages = model_instance.get_template(scene, text)
        Messenger().send(self.line_bot_api, self.event.reply_token, messages, method)

    def _get_message_event(self):
        return MESSAGE_MODELS.get(self.event.message.text, None)

    def _get_postback_event(self):
        return json.loads(self.event.postback.data)


class PostbackHandler(object):
    def __init__(self, event):
        self._EVENT = {
            'process': self.process
        }
        self.event = json.loads(event)
        self.event_type = self.event.get('type')
        self.event_data = self.event.get('data')

    def handle_event(self):
        logger.info('handle_event:{}'.format(self.event))
        return self._EVENT.get(self.event_type)(self.event_data)

    def process(self, data):
        model = data.get('model')
        process = data.get('process', None)
        model_instance = MODELS.get(model)()
        return model_instance.process_handler(process)
