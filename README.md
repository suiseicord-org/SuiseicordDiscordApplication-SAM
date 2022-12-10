# Discord_SAM 

すいせいこーどで動作するApplication Commandのプログラム。

全てのBOTで共通してこのプログラムコードを使用する。

## このプログラムを使用しているアプリケーション

- ロボ街#5325
- テスト街#0491
- 通知街#7275

## 環境変数
* `APPLICATION_NAME`
    - `General`
    - `Test`
* `LOGGING_MODE`

## 実装済みコマンド

1. /send
    1. channel
        - チャンネルやスレッドにメッセージを送信する。
    2. dm
        - サーバーメンバーにDMを送信する。
2. /user
    1. mention
        - サーバーメンバーの情報を表示する。
    2. id
        - サーバーの所属に関わらず、ユーザーIDから検索し表示する。
3. /channel
    1. topic
        - チャンネルトピックを編集する。
99. /test
    * テスト用コマンド。
