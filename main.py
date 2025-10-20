import sys
from flask import Flask, render_template, redirect
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
from data import db_session
from data.login_form import LoginForm
from data.users import User
from data.register import RegisterForm
from sqlalchemy import update
from flask import Flask
import shutil
import requests
import random
import json
import jinja2
from flask import request
from datetime import datetime
import os

random_coordinate = ''
K = ''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/white')
def white():
    return render_template('white.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong email or password!", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration', form=form,
                                   message="Passwords don't match!")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration', form=form,
                                   message="This email is already being taken by another user!")
        user = User(
            email=form.email.data,
            name=form.name.data,
            registerDate=datetime.now().strftime("%d.%m.%Y")
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route("/")
def main_page():
    return render_template("index.html", title='Main page')


@app.route("/playRandomMode")
@login_required
def playRandomMode():
    global random_coordinate
    random_coordinate1 = random.randint(55692711, 55868057)
    random_coordinate2 = random.randint(37544543, 37718527)
    random_coordinate1 /= 10 ** 6
    random_coordinate2 /= 10 ** 6
    random_coordinate = [random_coordinate1, random_coordinate2]
    
    random_coordinate_copy = list(str(elem) for elem in random_coordinate)
    chosen_file = open("static/coordinates/chosen.txt", 'w')
    chosen_file.write(', '.join(random_coordinate_copy))
    chosen_file.close()
    
    return render_template("playRandomMode.html",
                           title='Play UGDY',
                           data=random_coordinate,
                           yandex_api_key=os.getenv('YANDEX_MAPS_API_KEY'))

# PLAY CODE END


@app.route("/account")
def account():
    return render_template("account.html", title='Main page')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/explorer.sqlite")
    app.run(port=5000)
    print(K)


if __name__ == '__main__':
    main()