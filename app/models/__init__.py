from .clock_in import ClockIn
from .main_menu import MainMenu
from .trash import Trash

MODELS = {
    'main_menu': MainMenu,
    'clock_in': ClockIn,
    'trash': Trash
}

MESSAGE_MODELS = {
    'メインメニュー': {
        'model': 'main_menu',
        'scene': 'menu'
    },
    '勤怠メニュー': {
        'model': 'clock_in',
        'scene': 'menu'
    },
    'ごみ出しメニュー': {
        'model': 'trash',
        'scene': 'menu'
    }
}
