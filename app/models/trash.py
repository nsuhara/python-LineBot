"""
author          : nsuhara <na010210dv@gmail.com>
date created    : 2019/5/1
python version  : 3.7.3
"""
import datetime
import json
import logging

from linebot.models.actions import PostbackAction, URIAction
from linebot.models.template import ButtonsTemplate, TemplateSendMessage

from app.framework.nslinebot.models.story_board import StoryBoard
from app.processes.trash import Process

logger = logging.getLogger(__name__)


class Trash(StoryBoard):
    def __init__(self):
        super().__init__()
        process = Process()
        self.PROCESS = {
            'what_day_of_garbage_is_today': process.what_day_of_garbage_is_today
        }

    def process_handler(self, kwargs):
        logger.info('process_handler:{}'.format(kwargs))
        return self.PROCESS.get(kwargs.get('handle'))()

    def story_board(self, text):
        return {
            'menu': TemplateSendMessage(
                alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    title='ごみ出しメニュー',
                    text=text if text else '選択して下さい',
                    actions=[
                        PostbackAction(
                            label='今日のごみ出し',
                            data=json.dumps({
                                'model': 'trash',
                                'scene': 'result',
                                'process': {'handle': 'what_day_of_garbage_is_today'}
                            })
                        ),
                        PostbackAction(
                            label='戻る',
                            data=json.dumps({
                                'model': 'main_menu',
                                'scene': 'menu'
                            })
                        )
                    ]
                )
            ),
            'result': TemplateSendMessage(
                alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    title='ごみ出しメニュー',
                    text=text if text else '取得できませんでした',
                    actions=[
                        PostbackAction(
                            label='戻る',
                            data=json.dumps({
                                'model': 'trash',
                                'scene': 'menu'
                            })
                        )
                    ]
                )
            )
        }
