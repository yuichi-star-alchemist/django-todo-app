アプリの構成のモデル  
https://github.com/var-co-jp/todo-app-sample  
Djangoの学習のためなので構成を考える部分は省略しました  
Dockerコンテナ上でDjangoを使用してtodoウェブアプリを動かすサンプルです
もし参考になれば見てみてください  
パスワードポリシーを緩めている、  
秘密鍵が書いてある等、全く本番環境用ではありません  
サーバーはリロードモード、プロジェクトディレクトリ内をマウントするので  
ファイルの変更はDocker上のサーバーにすぐ反映されます  
初学者がチュートリアルとchatGPTを頼りに作成したものです  


利用手順  

①README.mdと同じディレクトリにて実行  
```sh
docker compose up
```
②別のターミナルからコンテナにアクセス  
```sh
docker exec -it todo_app bash
```
③アクセスターミナルでデータベース初期化  
管理ユーザー作成  
(ユーザー名、)
```sh
python manage.py makemigrations App
python manage.py migrate
python manage.py createsuperuser
```
④ブラウザでアクセス
```
http://localhost:8000
```

※必要であればデータベース消去用  
ユーザーもデータもすべて消えます  
使用後は再度③を実行  
```sh
rm -fr db.sqlite3 App/migrations/
```