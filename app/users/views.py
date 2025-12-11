from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from . import users_bp
from .forms import RegistrationForm, LoginForm
from app import db, bcrypt
from app.posts.models import User

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.list_posts'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Аккаунт створено! Тепер можна увійти.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.list_posts'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Ви успішно увійшли!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('posts.list_posts'))
        else:
            flash('Невірний email або пароль', 'danger')
    return render_template('login.html', form=form)

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з аккаунту', 'info')
    return redirect(url_for('posts.list_posts'))