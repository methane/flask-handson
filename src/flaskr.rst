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

.. literalinclude:: flaskr/run.py

flaskr/__init__.py
^^^^^^^^^^^^^^^^^^^

Python では `__init__.py` というファイルを含むディレクトリがパッケージになります。
パッケージとは、子モジュールを持てるモジュールです。
この場合 `flaskr/__init__.py` は `flaskr` というパッケージになり、
`flaskr/config.py` は `flaskr.config` モジュールになります。

`flaskr/__init__.py` は `app` オブジェクトの生成とプラグインのセットアップをし、
最後に `views` を読み込みます。

.. literalinclude:: flaskr/flaskr/__init__.py

flaskr/config.py
^^^^^^^^^^^^^^^^^

`flaskr/config.py` には設定を書いていきます。

`SQLALCHEMY_DATABASE_URI` は SQLAlchemy 用の設定で、
"ドライバ名://ホスト名/db名?オプション=値" という URI 形式で利用するデータベースを指定します。
今回は sqlite を使うので、ドライバ名は sqlite, ホスト名は空、db名はファイル名になります。

`SECRET_KEY` は、セッション情報を暗号化するための鍵です。
Flask はデフォルトではセッション情報を全て Cookie に保存するので、改ざん対策のために暗号化しています。

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

flaskr/models.py:

.. literalinclude:: flaskr/flaskr/models.py

実際にデータベースとテーブルを作ります::

    python -c "import flaskr.models; flaskr.models.init()"


Step 2: view
==============

Blog エントリの一覧と投稿ができるように、 flaskr/views.py を実装していきます。

flaskr/views.py:

.. literalinclude:: flaskr/flaskr/views.py


Step 3: テンプレートとCSSを用意する
=====================================

.. Flask は Jinja2 というテンプレートエンジンを使います。

flaskr/templates/show_entries.html:

.. literalinclude:: flaskr/flaskr/templates/show_entries.html

CSS も用意しましょう.

flaskr/static/style.css:

.. literalinclude:: flaskr/flaskr/static/style.css



.. .. note::

..    Jinja2 の構文は、 Django のテンプレートエンジンや Twig の構文と似ています。
..    もともと Jinja は Django を参考に作られていて、 Twig は Jinja を参考に作られているからです。

.. Jinja2 はテンプレートの継承という機能を持っています。
.. まずは次のようなファイルを作ってください。
.. .. literalinclude:: basic/template/layout.html

