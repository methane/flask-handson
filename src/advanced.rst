Flask を使いこなそう
=====================

URLマッピング
--------------

`@app.route` で指定する URL にパラメータを埋め込むこともできます。

`<引数名>` を URL に入れると、その部分の文字列が引数に渡されます。
`<int:引数名>` と書くと、その部分が整数に変換されるようになります。

flaskr で特定の POST だけを表示するアクションを書いてみます。

flaskr/views.py::

    @app.route('/entry/<int:id>')
    def show_entry(id):
        entry = Entry.get_or_404(id=id)
        flask.render_template('entry.html', entry=entry)

view の分割
-------------

flaskr は小さかったので、 views.py 1つですべてのアクションを書いていましたが、
アプリケーションが大きくなってきたらパッケージを使って分割すると良いでしょう。

flaskr の場合、 views というディレクトリを作成し、 views.py を views/flaskr.py
にリネームすると良いでしょう。 views/ ディレクトリを「パッケージ」にするために、
__init__.py という空のファイルも作っておきます。

::

    views/
        __init__.py
        flaskr.py

Flask-GoogleAuth
------------------

Flask に認証機能を追加するプラグインはいくつかありますが、パスワード認証を使うと
ユーザーに新しくパスワードを作って管理してもらわないといけないので、
OpenID などの外部の認証機能を使うプラグインを利用するといいでしょう。

Flask-GoogleAuth は Google アカウントでログインするためのプラグインです。
社内ユーザー向けのアプリを作りたい場合は、Google Apps のドメインを使うこともできます。

インストール
^^^^^^^^^^^^^

::

    $ pip install Flask-GoogleAuth

プラグインを組み込む
^^^^^^^^^^^^^^^^^^^^^^

flaskr/__init__.py::

    from flask import Flask
    from flask.ext.sqlalchemy import SQLAlchemy
    from flask.ext.googleauth import (GoogleFederated, GoogleAuth)

    app = Flask(__name__)
    app.config.from_object('flaskr.config')
    db = SQLAlchemy(app)

    auth = GoogleAuth(app)
    #klab.com ドメインの Google Apps で認証する場合は GoogleFederated を使う
    #auth = GoogleFederated(app, 'klab.com')

view から使う
^^^^^^^^^^^^^^

ある view に認証しないとアクセスできないようにするには次のようにします。 ::

    from flaskr import auth, app

    @app.route('/add', methods=['POST'])
    @auth.required
    def add_entry():
        ...

認証された場合、 `flask.g.user` というオブジェクトができます。このオブジェクトには
`user.email`, `user.name`, `user.first_name`, `user.last_name` という属性があります。

`flask.g` というオブジェクトはデフォルトでテンプレートに渡されるようになっているので、
テンプレートの中では `{{ g.email }}` のようにしてユーザーの情報を表示することができます。

Flask-Admin
------------

Flask-Admin を使えば、データベースのCRUD管理画面を簡単に作成出来ます。

TODO


