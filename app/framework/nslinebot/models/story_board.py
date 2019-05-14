"""
abstract class

author          : nsuhara <na010210dv@gmail.com>
date created    : 2019/5/1
python version  : 3.7.3
"""
import abc
import logging

from linebot.models.send_messages import TextSendMessage

logger = logging.getLogger(__name__)


class StoryBoard(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def process_handler(self, kwargs):
        pass

    @abc.abstractmethod
    def story_board(self, text):
        pass

    def get_message(self, text):
        logger.info('get_message:{}'.format(text))
        return TextSendMessage(text=text)

    def get_template(self, scene, text=None):
        logger.info('get_template:{}'.format(scene))
        return self.story_board(text).get(scene, None)
