# Discord_SAM 

すいせいこーどで動作するApplication Commandのプログラム。

全てのBOTで共通してこのプログラムコードを使用する。

## このプログラムを使用しているアプリケーション

- ロボ街#5325
- テスト街#0491
- 通知街#7275

## 環境変数
* `DISCORD_TOKEN`
* `APPLICATION_ID`
* `APPLICATION_PUBLIC_KEY`
* `RDS_HOST`
* `DB_USER`
* `DB_PASSWORD`
* `DB_NAME`

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
