from flask import url_for, render_template, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from User import *
from Note import *
from config import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def main_page():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id).all()
        is_auth = True
    else:
        notes = []
        is_auth = False

    return render_template('all_notes.html', title='ZNote', notes=notes, is_auth=is_auth)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        note = Note(title=title, text=text, user_id=current_user.id)

        try:
            db.session.add(note)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка при создании заметки'
    return render_template('create_note.html', title='ZNote | Create Note')

@app.route('/<id>')
@login_required
def note(id):
    note = Note.query.get_or_404(id)
    return render_template('note.html', title='ZNote', note=note, id=id)

@app.route('/<id>/del')
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/')
    except:
        return 'Произошла ошибка при удалении'

@app.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        note.edit(title=title, text=text)

        try:
            db.session.commit()
            return redirect(url_for('note', id=id))
        except:
            return 'Произошла ошибка при попытки изменить заметку'
    return render_template('edit_note.html', title='ZNote | Edit Note', note=note)

@app.route('/register', methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return 'Почта уже зарегистрирована'

        user = User(username=username, email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/')
        except:
            return 'Произошла ошибка при попытки регистрации'
    return render_template('registration.html', title='ZNote | Registration')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            if user:
                return 'Неверно введен пароль'
            return 'Почта не зарегистрирована'
    return render_template('login.html', title='ZNote | Login')

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect('/')
    except:
        return 'Не получилось выйти'

if __name__ == '__main__':
    app.run(debug=True)