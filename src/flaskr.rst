########
 flaskr
########

公式の Flask のチュートリアルにある flaskr というミニブログを写経していきます。

公式のチュートリアルでは SQLite を直接使っていましたが、
今回は SQLAlchemy という O/R マッパーを使っていきます。

SQLAlchemy は Python の O/R マッパーの中では最も強力なものですが、
簡単な使い方もできるようになっています。

Step 0: 準備
=============

インストール
-------------

Flask-SQLAlchemy という Flask 拡張をインストールします。 ::

    $ pip install Flask-SQLAlchemy

ディレクトリ構成
------------------

Hello, World プログラムでは1ファイルで完結していましたが、今回は少しファイルを分けて、
本格的な構成にしていきます。

まず、適当なディレクトリの中に次のようにファイルとディレクトリを作っていきます::

    run.py
    flaskr/
        __init__.py
        config.py
        views.py
        models.py
        templates/
        static/

run.py
^^^^^^^

デバッグモードでアプリケーションを起動するだけのスクリプトです。
(`ダウンロード <src/flaskr/run.py>`_)

.. literalinclude:: flaskr/run.py

flaskr/__init__.py
^^^^^^^^^^^^^^^^^^^

Python では `__init__.py` というファイルを含むディレクトリがパッケージになります。
パッケージとは、子モジュールを持てるモジュールです。
この場合 `flaskr/__init__.py` は `flaskr` というパッケージになり、
`flaskr/config.py` は `flaskr.config` モジュールになります。

`flaskr/__init__.py` は `app` オブジェクトの生成とプラグインのセットアップをし、
最後に `views` を読み込みます。
(`ダウンロード <src/flaskr/flaskr/__init__.py>`_)

.. literalinclude:: flaskr/flaskr/__init__.py

flaskr/config.py
^^^^^^^^^^^^^^^^^

`flaskr/config.py` には設定を書いていきます。

`SQLALCHEMY_DATABASE_URI` は SQLAlchemy 用の設定で、
"ドライバ名://ホスト名/db名?オプション=値" という URI 形式で利用するデータベースを指定します。
今回は sqlite を使うので、ドライバ名は sqlite, ホスト名は空、db名はファイル名になります。

`SECRET_KEY` は、セッション情報を暗号化するための鍵です。
Flask はデフォルトではセッション情報を全て Cookie に保存するので、改ざん対策のために暗号化しています。
(`ダウンロード <src/flaskr/flaskr/config.py>`_)

.. literalinclude:: flaskr/flaskr/config.py

その他
^^^^^^^

flaskr/views.py と flaskr/models.py はこれから実装していくので、
いまは空にしておいてください。 views にはアクションを、 models には
モデルを書いていきます。

templates にはテンプレートファイルを、
static には CSS などの静的ファイルを格納していきます。

Step 1: model
=================

スキーマを定義するだけのモデルクラスを作ります。

flaskr/models.py (`ダウンロード <src/flaskr/flaskr/models.py>`_):

.. literalinclude:: flaskr/flaskr/models.py

実際にデータベースとテーブルを作ります::

    python -c "import flaskr.models; flaskr.models.init()"

インタラクティブシェルでモデルを触ってみましょう.
SQLAlchemy は Unit of Work というスタイルの O/R マッパーで、取得したエンティティは自動的に「セッション」に紐づけられます。
エンティティを操作したあとに `db.session.commit()` することで、変更がDBに反映されます。
新規にエンティティを作成する場合は、 `db.session.add(entity)` でセッションに紐づけます。

    >>> from flaskr.models import Entry
    >>> from flaskr import db
    >>> entry = Entry(title="title1", text="text1")
    >>> db.session.add(entry)
    >>> db.session.commit()
    >>> for i in range(2, 5):
    ...     entry = Entry(title='title' + str(i), text='text' + str(i))
    ...     db.session.add(entry)
    ... 
    >>> db.session.commit()
    >>> entries = Entry.query.all()
    >>> entries
    [<Entry id=1 title='title1'>, <Entry id=2 title='title2'>, <Entry id=3 title='title3'>, <Entry id=4 title='title4'>]
    >>> entries[0].id
    1
    >>> entries[0].text
    u'text1'
    >>> Entry.query.get(3)
    <Entry id=3 title='title3'>
    >>> Entry.query.filter_by(title='title2').one()
    <Entry id=2 title='title2'>
    >>> entry = _
    >>> entry.text
    u'text2'
    >>> entry.text = "fizz buzz"
    >>> db.session.commit()
    >>> Entry.query.filter_by(title='title2').one().text
    u'fizz buzz'

Step 2: view
==============

Blog エントリの一覧と投稿ができるように、 flaskr/views.py を実装していきます。

flaskr/views.py (`ダウンロード <src/flaskr/flaskr/views.py>`_):

.. literalinclude:: flaskr/flaskr/views.py


Step 3: テンプレートとCSSを用意する
=====================================

.. Flask は Jinja2 というテンプレートエンジンを使います。

flaskr/templates/show_entries.html
(`ダウンロード <src/flaskr/flaskr/templates/show_entries.html>`_):

.. literalinclude:: flaskr/flaskr/templates/show_entries.html

CSS も用意しましょう.

flaskr/static/style.css
(`ダウンロード <src/flaskr/flaskr/static/style.css>`_):

.. literalinclude:: flaskr/flaskr/static/style.css


.. .. note::

..    Jinja2 の構文は、 Django のテンプレートエンジンや Twig の構文と似ています。
..    もともと Jinja は Django を参考に作られていて、 Twig は Jinja を参考に作られているからです。

.. Jinja2 はテンプレートの継承という機能を持っています。
.. まずは次のようなファイルを作ってください。
.. .. literalinclude:: basic/template/layout.html

これでひとまず完成です。

::

    $ python run.py

で実行して、ブラウザで動いていることを確認してみましょう。


Step 4: テスト
================

インタラクティブシェル
-----------------------

まずはインタラクティブシェルからリクエストを実行してみましょう. ::

    >>> import flaskr
    >>> client = flaskr.app.test_client()
    >>> response = client.post('/add', data={'title': 'test title 1', 'text': 'test text 1'}, follow_redirects=True)
    >>> response.status_code
    200
    >>> response.status
    '200 OK'
    >>> print response.data
    <!doctype html>
    <html>
    <head>
        <title>Flaskr</title>
        <link rel=stylesheet type=text/css href="/static/style.css">
    </head>
    <body>
        <div class=page>
          <h1>Flaskr</h1>
          
            <div class=flash>New entry was successfully posted</div>
          
          <form action="/add" method=post class=add-entry>
            <dl>
              <dt>Title:
              <dd><input type=text size=30 name=title>
              <dt>Text:
              <dd><textarea name=text rows=5 cols=40></textarea>
              <dd><input type=submit value=Share>
            </dl>
          </form>
          <ul class=entries>
          
            <li><h2>test title 1</h2>test text 1
          
          </ul>
        </div>
    </body>
    </html>

py.test のインストール
-----------------------

Python の標準ライブラリにも unittest モジュールがありますが、より簡単にテストを書ける
`pytest` を使いましょう。

::

    $ pip install pytest

テストを書く
-------------

py.test は、 `*_test` や `test_*` という名前のモジュールを検索して、その中の
`test_*` という名前の関数や `Test*` といった名前のクラスを検索し実行します。

py.test を使う場合、 `assertEqual` などの assert メソッドを利用しなくても、
python の `assert` 文を使うだけで十分です。
たくさんのメソッドを覚える必要が無いので楽ちんです。

先ほどインタラクティブシェルで試したログを見ながらテストを書いていきます。

flaskr/tests/test_actions.py
(`ダウンロード <src/flaskr/flaskr/tests/test_actions.py>`_):

.. literalinclude:: flaskr/flaskr/tests/test_actions.py
    :linenos:

実行する
----------

`py.test` を実行すると、テストファイルを見つけた場所でテストを実行するので、
`import flaskr` が失敗してしまいます。
プロジェクトのトップディレクトリを検索パスに追加するために :envvar:`PYTHONPATH`
を使いましょう。

::

        $ PYTHONPATH=. py.test
        ================================== test session starts ===================================
        platform darwin -- Python 2.7.3 -- pytest-2.3.4
        collected 1 items 
        
        flaskr/tests/test_actions.py .
        
        ================================ 1 passed in 0.20 seconds ================================

.. note::

    PYTHONPATH 以外の方法

    `setup.py` というファイルを書いて、一般的なインストールできるパッケージの形にすると、
    `python setup.py develop` で Python の検索パスに現在のディレクトリを追加されます。

    また、 `py.test --genscript=runtests.py` でテストを実行するスクリプトを生成し、
    その先頭で次のように検索パスを追加しても良いでしょう。 ::

        import sys, os
        sys.path.insert(0, os.path.dirname(__file__))

IDD
---

モデルやアクションを書く前にテストを書くTDDをするためには、まずモデルやレスポンスオブジェクトのAPIを覚えないといけません。

初心者のうちは、インタラクティブシェルで触ってみて、コードを書いて、インタラクティブシェルで動作を確認して、
その結果をテストにするというインタラクティブシェル駆動開発を行えば、APIを覚えながら開発ができます。
