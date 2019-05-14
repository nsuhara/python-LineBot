"""
author          : nsuhara <na010210dv@gmail.com>
date created    : 2019/5/1
python version  : 3.7.3
"""
import datetime
import logging

logger = logging.getLogger(__name__)


class Process(object):
    def __init__(self):
        pass

    def what_day_of_garbage_is_today(self):
        WEEKDAY = [
            '月曜日',
            '火曜日',
            '水曜日',
            '木曜日',
            '金曜日',
            '土曜日',
            '日曜日'
        ]
        GARBAGE = [
            '燃えるごみ',
            'プラごみ',
            '燃えるごみ',
            'その他プラごみ',
            '燃えるごみ',
            '資源ごみ',
            'なし'
        ]
        DETAIL = {
            '燃えるごみ': '生ごみ、紙くず',
            'プラごみ': '容器包装プラ、リサイクルプラ',
            'その他プラごみ': '30cm未満のプラやゴム、合成皮革',
            '資源ごみ': 'ビン、缶、金属、かさ、小型家電、布',
            '陶磁器/ガラスごみ': '刃物、30cm以上50cm未満のプラ',
            'なし': 'なし'
        }
        date_time = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        weekday = date_time.weekday()
        week_number = self._get_week_number(date_time)
        if weekday == 2 and week_number == 4:
            return '第4{}は「{}」の日です\n({})'.format(WEEKDAY[weekday], '陶磁器/ガラスごみ', DETAIL.get('陶磁器/ガラスごみ'))
        else:
            return '{}は「{}」の日です\n({})'.format(WEEKDAY[weekday], GARBAGE[weekday], DETAIL.get(GARBAGE[weekday]))

    def _get_week_number(self, date_time):
        day = date_time.day
        week_number = 0
        while day > 0:
            week_number += 1
            day -= 7
        return week_number
