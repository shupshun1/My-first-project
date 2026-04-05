from flask import Flask, render_template, redirect, session, request, jsonify
from forms import LoginForm, RegisterForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
) # путь к общей папке базе данных

from database import db_session, User # импорт папки БД

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key'


db_session.global_init("../database/game.db")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.root_path, 'static', 'img', filename))
        db_sess = db_session.create_session()
        existing_user = db_sess.query(User).filter(User.username == form.username.data).first()
        if existing_user:
            print("Занято")
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   error='Логин уже занят!')
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            username=form.username.data,
            gender=form.gender.data,
            message=form.message.data,
            photo=filename
        )
        user.hashed_password = generate_password_hash(password=form.password.data)
        db_sess.add(user)
        db_sess.commit()
        session['user_id'] = user.id
        print(user)
        return redirect('/success')
    return render_template('register.html', title="Регистрация", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            session['user_id'] = user.id
            return redirect('/profile')
        return render_template(
            "login.html",
            title='Вход',
            form=form,
            error='Неверный логин или пароль'
        )
    return render_template("login.html", title='Вход', form=form)


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    db_sess = db_session.create_session()
    user = db_sess.get(User, session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect('/login')
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.route('/success')
def success():
    return render_template('success.html', title="Аккаунт создан!")

@app.route('/api/update-stats', methods=['POST'])
def update_stats():
    data = request.json
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == data['username']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.update_stats(
        kills=data.get("kills", 0),
        deaths=data.get('deaths', 0),
        bosses=data.get('bosses_defeated', 0),
        score=data.get('score', 0)
    )
    db_sess.commit()
    return jsonify({
        'status': 'ok',
        'message': 'Stats updated',
        'new_level': user.level,
        'total_score': user.total_score,
        'kills': user.kills,
        'deaths': user.deaths,
        'bosses_defeated': user.bosses_defeated
    })

@app.route("/api/user/<username>", methods=['GET'])
def get_user_stats(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        'username': user.username,
        'level': user.level,
        'kills': user.kills,
        'deaths': user.deaths,
        'bosses_defeated': user.bosses_defeated,
        'total_score': user.total_score
    })


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')