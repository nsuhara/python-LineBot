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
from app.processes.clock_in import Process

logger = logging.getLogger(__name__)


class ClockIn(StoryBoard):
    def __init__(self):
        super().__init__()

    def process_handler(self, kwargs):
        logger.info('process_handler:{}'.format(kwargs))
        dakoku_value = {
            'check_in': 'syussya',
            'check_out': 'taisya'
        }
        process = Process()
        # stub start.
        import datetime
        from unittest.mock import MagicMock
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        dakoku_jp = {
            'check_in': '出社時刻',
            'check_out': '退社時刻'
        }
        process.post = MagicMock(return_value={
            'message': '(スタブ){}を登録しました'.format(dakoku_jp.get(kwargs.get('handle'))),
            'timestamp': '{}/{}/{} {}:{}:{}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        })
        # stub end.
        res = process.post(dakoku_value.get(kwargs.get('handle')),
                           kwargs.get('user_id'))
        return '{}\n{}'.format(res.get('message'), res.get('timestamp'))

    def story_board(self, text):
        return {
            'menu': TemplateSendMessage(
                alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    title='勤怠メニュー',
                    text=text if text else '選択して下さい',
                    actions=[
                        URIAction(
                            uri='line://app/<LIFF URL>',
                            label='勤怠入力'
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
            )
        }
