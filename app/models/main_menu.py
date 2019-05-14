"""
author          : nsuhara <na010210dv@gmail.com>
date created    : 2019/5/1
python version  : 3.7.3
"""
import json
import logging

from linebot.models.actions import PostbackAction
from linebot.models.template import ButtonsTemplate, TemplateSendMessage

from app.framework.nslinebot.models.story_board import StoryBoard

logger = logging.getLogger(__name__)


class MainMenu(StoryBoard):
    def __init__(self):
        super().__init__()

    def process_handler(self, kwargs):
        pass

    def story_board(self, text):
        return {
            'menu': TemplateSendMessage(
                alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    title='メインメニュー',
                    text=text if text else '選択して下さい',
                    actions=[
                        PostbackAction(
                            label='勤怠メニュー',
                            data=json.dumps({
                                'model': 'clock_in',
                                'scene': 'menu'
                            })
                        ),
                        PostbackAction(
                            label='ごみ出しメニュー',
                            data=json.dumps({
                                'model': 'trash',
                                'scene': 'menu'
                            })
                        ),
                        PostbackAction(
                            label='(工事中)クーポンメニュー',
                            data=json.dumps({
                                'model': 'coupon',
                                'scene': 'menu'
                            })
                        ),
                        PostbackAction(
                            label='(工事中)自然言語メニュー',
                            data=json.dumps({
                                'model': 'talk',
                                'scene': 'menu'
                            })
                        )
                    ]
                )
            )
        }
