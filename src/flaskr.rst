########
 flaskr
########

公式の Flask のチュートリアルにある flaskr というアプリケーションを写経していきます。
ただし、公式のチュートリアルでは SQLite をそのまま使っていましたが、今回は PeeWee
という O/R マッパーを使います。

Flask-PeeWee のインストール
=============================

Flask-Peewee という Flask 拡張をインストールします。

Windows::

    > python -m easy_install Flask-Peewee

Unix::

    $ pip install Flask-Peewee

Step 0: 準備
=============

適当なディレクトリを作って、その中に次のようにファイルとディレクトリを作っていきます::

    run.py
    flaskr/
        __init__.py
        views.py
        models.py
        templates/
        static/

run.py:

.. literalinclude:: flaskr/run.py

flaskr/__init__.py:

.. literalinclude:: flaskr/flaskr/__init__.py

flaskr/views.py と flaskr/models.py はこれから実装していくので、
いまは空にしておいてください。 views にはアクションを、 models には
モデルを書いていきます。

templates にはテンプレートファイルを、
static には CSS などの静的ファイルを格納していきます。

Step 1: model
=================

スキーマを定義するだけのモデルクラスを作ります。

flaskr/models.py::

    from flaskr import db
    from peewee import *


    class Entry(db.Model):
        title = CharField()
        text = CharField()


    def init():
        Entry.create_table()


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

.. .. note::

..    Jinja2 の構文は、 Django のテンプレートエンジンや Twig の構文と似ています。
..    もともと Jinja は Django を参考に作られていて、 Twig は Jinja を参考に作られているからです。

flaskr/templates/show_entries.html:

.. literalinclude:: flaskr/flaskr/templates/show_entries.html

.. Jinja2 はテンプレートの継承という機能を持っています。
.. まずは次のようなファイルを作ってください。
.. .. literalinclude:: basic/template/layout.html

CSS も用意しましょう.

flaskr/static/style.css:

.. literalinclude:: flaskr/flaskr/static/style.css
