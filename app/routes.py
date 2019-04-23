from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, Fb_Register_Form
from app.models import User
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix


@app.route('/')
@app.route('/index')
@login_required
def index():
    meals = [
        {
            'author': {'username': 'John'},
            'body': 'ate with you at Kaju',
            'timestamp': 'April 23'
        }
    ]
    return render_template('index.html', title='Home', meals=meals)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def authorize():
    client_id = 'HERE!!!'
    client_secret = 'HERE!!!!'
    authorization_base_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/oauth/access_token'
    redirect_uri = 'http://localhost:5000/fb_register'     # Should match Site URL
    fb = OAuth2Session(client_id, redirect_uri=redirect_uri)
    fb= facebook_compliance_fix(fb)
    authorization_url, state = fb.authorization_url(authorization_base_url)
    return authorization_url

@app.route('/register', methods=['GET', 'POST'])    
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    authorization_url=authorize()
    print(authorization_url)
    return render_template('register.html', title='Register', form=form, auth_url=authorization_url)

@app.route('/fb_register', methods=['GET', 'POST'])
def fb_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Fb_Register_Form()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('fb_register.html', title='Fb Register', form=form)
