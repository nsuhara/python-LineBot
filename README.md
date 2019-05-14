# はじめに

*(Mac環境の記事ですが、Windows環境も同じ手順になります。環境依存の部分は読み替えてお試しください。)*

この記事を最後まで読むと、次のことができるようになります。

- Messaging APIについて理解する
- LINE Front-end Framework(LIFF)について理解する
- LINE BOT SDKを使って実装する

`イメージ画像`

| 勤怠メニュー                                                                                                                                           |     | 勤怠入力                                                                                                                                               |     | 結果                                                                                                                                                   |
| :-:                                                                                                                                                    | :-: | :-:                                                                                                                                                    | :-: | :-:                                                                                                                                                    |
| <img width="200" alt="IMG_1025.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/9504843e-f213-142c-fff9-e30391d90f92.png"> | >>> | <img width="200" alt="IMG_1026.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/14409c8f-d621-3dcb-121c-821a0a3ffd9d.png"> | >>> | <img width="200" alt="IMG_1027.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/bc1adf78-9c71-3e07-225a-aa107fc7239e.png"> |

| ごみ出しメニュー                                                                                                                                       |     | 今日のごみ出し                                                                                                                                         |
| :-:                                                                                                                                                    | :-: | :-:                                                                                                                                                    |
| <img width="200" alt="IMG_1028.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/12cd1875-d748-95fe-1d70-ffd1e95779d6.png"> | >>> | <img width="200" alt="IMG_1029.PNG" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/d102b1da-60a0-9fe8-3e7d-8e581abadc14.png"> |

# 関連する記事

- [Messaging API](https://developers.line.biz/ja/docs/messaging-api/)
- [LINE Front-end Framework(LIFF)](https://developers.line.biz/ja/docs/liff/)

# 実行環境

|     環境     |   Ver.  |
|--------------|---------|
| macOS Mojave | 10.14.4 |
| line-bot-sdk | 1.8.0   |
| Flask        | 1.0.2   |

# ソースコード

実際に実装内容やソースコードを追いながら読むとより理解が深まるかと思います。是非ご活用ください。

[GitHub](https://github.com/nsuhara/python-LineBot.git)

# Messaging APIとは

ユーザと双方向コミュニケーションを実現するための機能。Push Messageで、任意のタイミングでユーザにメッセージを送信することができる。Reply Messageで、ユーザからのメッセージに対して応答することができる。リクエストは、JSON形式でHTTPSを使って送信される。

# LINE Front-end Framework(LIFF)とは

LINE Front-end Framework(LIFF)内で動作するWebアプリ(HTML)のプラットフォーム。LIFFに登録したWebアプリをLINEの中で起動することができる。(2018年6月リリース)

# LINE BOTの実装

作成したFrameworkを使ってLINE BOTを実装する

## Frameworkの概要

- アプリ構成

    ```
    app
    ├── framework
    │   └── nslinebot
    │       ├── controllers
    │       │   └── handler.py
    │       ├── models
    │       │   └── story_board.py
    │       └── views
    │           └── messenger.py
    ├── liff
    │   └── clock_in.html
    ├── models
    │   ├── __init__.py
    │   ├── clock_in.py
    │   ├── main_menu.py
    │   └── trash.py
    └── processes
        └── clock_in.py
    ```

- ディレクトリ概要

    | ディレクトリ |                  説明                 |
    |--------------|---------------------------------------|
    | nslinebot    | LINE BOT SDKを拡張したFrameworkを格納 |
    | liff         | サービスと連携するWebアプリを格納     |
    | models       | サービスのメインフレームを格納        |
    | processes    | サービス独自の処理フレームを格納      |

## サービスの実装例

### 画面遷移の実装

__ポイント__
- Frameworkの`StoryBoard`を継承してサービスを`JSON形式`で実装する
- イベント情報をもたせるためPostbackで実装する
- `PostbackAction`の`data`に遷移先のサービスを記述する

|   data  |         説明         |
|---------|----------------------|
| model   | サービス名           |
| scene   | サービスの中の機能名 |
| process | サービス独自の処理名 |

```
app/models/main_menu.py

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
                        )
                    ]
                )
            )
        }
```

### サービス処理の実装

__ポイント__
- `PostbackAction(data)`の`process`にサービス独自の処理名を記述する
- `process_handler`にサービス独自の処理を実装する

```
app/models/trash.py

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
```

```
app/processes/trash.py

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
```

### サービス環境の実装

__ポイント__
- `__init__.py`にサービスの環境設定を記述する
- `MODELS`にサービス名を記述する
- `MESSAGE_MODELS`にサービスを起動するためのキーワード(メッセージ)を記述する

```
app/models/__init__.py

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
```

## LINE Front-end Framework(LIFF)の実装例

### LIFFアプリ(HTML)の実装

__ポイント__
- `LIFF SDK(https://d.line-scdn.net/liff/1.0/sdk.js)`を読み込む

*バージョン1.0のliff.sendMessages(messages)は、Postbackイベントが使用できないため、直接HerokuアプリにPostbackして対処。(2019/5/1)*

<img width="500" alt="スクリーンショット 2019-05-14 10.03.52.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/e1858035-0f34-b6d1-c10a-61d63bdfd528.png">

```
app/liff/clock_in.html

<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>clock_in</title>
    <style type="text/css">
        th {
            padding: 5% 5%;
        }

        button {
            color: black;
            font-size: 100%;
            width: 100%
        }

        div.label_user_id {
            color: black;
            font-size: 100%;
            text-align: right;
        }

        div.input_user_id {
            text-align: left;
        }

        input {
            color: black;
            font-size: 100%;
            width: 90%;
        }
    </style>
</head>

<body>
    <table align="center" border="1" width="100%">
        <tr>
            <th width="50%">
                <div class="label_user_id">社員番号:</div>
            </th>
            <th width="50%">
                <div class="input_user_id"><input type="number" id="user_id" required autofocus></div>
            </th>
        </tr>
        <tr>
            <th colspan="2"><button id="check_in">出社時刻</button></th>
        </tr>
        <tr>
            <th colspan="2"><button id="check_out">退社時刻</button></th>
        </tr>
    </table>

    <script src="https://d.line-scdn.net/liff/1.0/sdk.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
    <script type="text/javascript">
        window.onload = function (e) {
            liff.init(function (data) {
                initializeApp(data);
            });
        };

        function initializeApp(data) {
            document.getElementById("user_id").value = "";
            document.getElementById("check_in").addEventListener("click", function () { clock_in("check_in") });
            document.getElementById("check_out").addEventListener("click", function () { clock_in("check_out") });
        }

        function clock_in(handle) {
            if (!window.confirm("社員番号:" + document.getElementById("user_id").value + "\n本当によろしいですか?")) {
                return
            }
            var event = JSON.stringify({
                "type": "process",
                "data": {
                    "model": "clock_in",
                    "process": {
                        "handle": handle,
                        "user_id": document.getElementById("user_id").value
                    }
                }
            })
            $.post("https://<app-name>.herokuapp.com/postback", event)
                .done(function (data) {
                    window.alert(data);
                    liff.closeWindow();
                })
                .fail(function () {
                    window.alert("Error sending message: " + error);
                })
        }
    </script>
</body>

</html>
```

### LIFFの登録

1. LINE Developers > プロバイダーリスト > Your Provider > Your Channel > LIFF

1. LIFFの編集 > 保存する

1. `LIFF URL`をメモする

<img width="500" alt="スクリーンショット 2019-05-14 9.52.05.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/326996/7796edcf-5d17-3710-71d4-c98f8e626201.png">

### LIFFの実装

__ポイント__
- `URIAction`に`LIFF URL`を記述する

```
app/models/clock_in.py

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
```
