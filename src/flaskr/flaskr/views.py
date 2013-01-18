import flask
from flaskr import app
from flaskr.models import Entry


@app.route('/')
def show_entries():
    entries = Entry.select().order_by(Entry.id.desc()).limit(10).execute()
    return flask.render_template('show_entries.html',
                                 entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    Entry.create(
            title=flask.request.form['title'],
            text =flask.request.form['text'],
            )
    flask.flash('New entry was successfully posted')
    return flask.redirect(flask.url_for('show_entries'))
