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

Flask-Admin
------------

Flask-Admin を使えば、データベースのCRUD管理画面を簡単に作成出来ます。

TODO


