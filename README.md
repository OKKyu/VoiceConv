# Name
 VoiceConv by Google Speech-to-Text API

# Overview
   モバイルアプリから送信された音声ファイルを、Google Speech APIを用いてテキスト変換するWebアプリです。  
   本アプリはGCPとFlaskのプログラミングの学習のために作成しているものです。自由に流用しても良いですが、  
   全て自己責任でお願いします。  

# Requirement
- python3、python3-venv  
python2以前のバージョンでは動作確認していません。  
セットアップ用のシェルスクリプトも用意していますが、python3、python3-venvは既にインストール済みという前提で組んでいます。  
python3、python3-venvがない場合はユーザー様各自でパッケージ管理ソフトからインストールをして下さい。  
- その他依存ライブラリはrequirements.txtに記載してあります。  
特に重要なライブラリは以下の通りです。  
google-cloud-speech  ：音声ファイルを文字列へ変換するAPI。  
Flask                ：リクエストを受け、文字列をレスポンスとして返すWebアプリ。  
gunicorn             ：flaskをデプロイするWebサーバー。  

# Download
  ルートフォルダ "VoiceConv" ごと好きな場所に格納して下さい。

# Setup
 コンソールでVoiceConvフォルダ直下をカレントディレクトリとし、以下を実行して下さい。  
 
   bash setup.sh  
 
 本シェルスクリプトは以下の処理を行います。  
 ・VoiceConv 内部にpythonのvenvで仮想環境を作成します。  
 ・pipコマンドを実行し、requirements.txtをもとにpythonの依存ライブラリをダウンロードします。  

# Usage 
- 起動前の設定  
    本アプリではgoogle-cloud-speech API を使用していますが、このAPIを実行するにはGoogle Cloud Platformへの
    アカウント登録およびAPIの有効化、そしてサービスアカウントキーとなるJSONファイルの読み込みが必要です。
    
    キーファイルについては以下を参照して下さい。  
    &emsp;https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries
    尚、取得したキーファイルを環境変数へ設定する際にはrun.shの以下行に設定して下さい。  
    &emsp;GOOGLE_APPLICATION_CREDENTIALS='' ←空文字列となっている箇所に取得したキーファイルのパスを指定して下さい。  

- アプリの起動  
    コンソールでVoiceConvフォルダ直下をカレントディレクトリとし、以下を実行して下さい。  

     bash run.sh ワーカー数 ホスト名（もしくはIPアドレス） ポート番号  

   "ワーカー数"  1〜8を入力して下さい。  
   "ホスト名"    ホスト名またはIPアドレスを入力して下さい。  
   "ポート番号"  ポート番号を入力して下さい。  
   
   本アプリはWebアプリを起動するWSGIサーバーにgunicornを使用しています。  
   詳細はgunicornのサイトを参照して下さい。  

- 音声変換方法  
    音声の送信  
      スマホアプリから以下URLを送信して下さい。  
        `http://ホスト名:ポート番号/voiceConv`  
        
      httpメソッドはPOSTで送信して下さい。GETメソッドには未対応です。  
      input type=file 要素に音声ファイルを添えつけて送信して下さい。  
      現時点では音声のフォーマットは以下にのみ対応しています。  
        ファイルの種類 audio/wav  
        サンプルレート 44100  
      また、言語はja-JP (日本語）のみ対応しています。他言語では返却しません。  
      
    文字列の受信  
      文字列はjson形式で返却されます。  

# Note
 前提：
- osはlinux(64bit)のみ対応しています。macやwindowsでは動作保証しません。  
- 複数同時起動した場合には対応していません。  
- jsonは以下構造となっています。  
    {  
      0:"変換結果１",  
      1:"変換結果２",  
       ・・・以下繰り返し  
    }  
- 複数の変換結果が返却される場合も想定した処理になっていますが、基本は１件のみ返却されます。  
  入力音声はストリームとして読み込み、google-cloud-speech API へ引き渡しています。  
  本アプリ内部で音声ファイルを保管するような仕組みにはしていません。いったん音声ファイルとして
  flaskのローカルに保存してからgoogle-cloud-speech APIへ音声ファイルを読み込ませることも
  可能ですが、ハードディスクに書き込む時間がない分高速化できると考えてこのような仕組みにしています。  

# Structure

- `VoiceConv/main.py`          Flaskアプリのプログラム本体です。 (entry point)
- `VoiceConv/ttospeech.py`     google-cloud-speech APIを実行するためのサブパッケージです。
- `VoiceConv/templates`         機能テスト用の画面。必須ではありません。
- `VoiceConv/static`             機能テスト用の画面。必須ではありません。
- `VoiceConv/requrements.txt`  pythonの依存ライブラリのリストです。依存ライブラリのインストール時に参照されます。
- `VoiceConv/setup.sh`  依存ライブラリの自動インストール用のスクリプトです。
- `VoiceConv/run.sh`    ショートカットからの起動時に実行されるファイルです。VoiceConv.pyを実行します。

# Lisense
  VoiceConv version 1.0.0  
  (c) 2020 OKKyu allrights reserved under MIT license.  

  ライセンスの対象  
  main.py  
  setup.sh  
  run.sh  
  requrements.txt  

  注意：依存ライブラリはOKKyuの著作物ではありません。  
  
# Author
OKKyu
