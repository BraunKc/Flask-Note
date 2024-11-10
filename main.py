from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=datetime.now().date())

    def __repr__(self):
        return '<Note %r>' % self.id

@app.route('/')
def main_page():
    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template('all_notes.html', title='ZNote', notes=notes)

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        note = Note(title=title, text=text)

        try:
            db.session.add(note)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка при создании заметки'
    return render_template('create_note.html', title='ZNote | Create Note')

@app.route('/<id>')
def note(id):
    note = Note.query.get_or_404(id)
    return render_template('note.html', title='ZNote', note=note, id=id)

@app.route('/<id>/del')
def delete_note(id):
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/')
    except:
        return 'Произошла ошибка при удалении'

@app.route('/<id>/edit', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.text = request.form['text']
        note.date = datetime.utcnow()

        try:
            db.session.commit()
            return redirect(url_for('note', id=id))
        except:
            return 'Произошла ошибка при попытки изменить заметку'
    return render_template('edit_note.html', note=note)

if __name__ == '__main__':
    app.run()