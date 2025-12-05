from flask import (
    Blueprint, render_template, request, redirect, url_for, 
    session, flash, make_response
)
from datetime import datetime, timedelta


users_bp = Blueprint(
    'users',
    __name__,
    template_folder='templates' 
)

VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Завдання 1.2: Сторінка входу та обробка форми."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['username'] = username 
            flash('Вхід виконано успішно!', 'success') 
            return redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль.', 'danger') 
            return redirect(url_for('users.login'))
    
    
    return render_template('users/login.html', title="Вхід")

@users_bp.route('/profile')
def profile():
    """Завдання 1.3, 2, 3: Сторінка профілю."""
    
    
    if 'username' not in session:
        flash('Будь ласка, увійдіть, щоб побачити цю сторінку.', 'warning')
        return redirect(url_for('users.login'))

   
    username = session['username']
    
    
    cookies = request.cookies
    
    return render_template('users/profile.html', title="Профіль", username=username, cookies=cookies)

@users_bp.route('/logout')
def logout():
    """Завдання 1.4: Вихід з системи."""
    session.pop('username', None) 
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))



@users_bp.route('/add-cookie', methods=['POST'])
def add_cookie():
    if 'username' not in session: 
        return redirect(url_for('users.login'))

    key = request.form.get('key')
    value = request.form.get('value')
    expiry_days = request.form.get('expiry_days')
    
    if not key or not value:
        flash('Ключ та значення кукі є обов\'язковими.', 'danger')
        return redirect(url_for('users.profile'))

    resp = make_response(redirect(url_for('users.profile')))
    
    expires = None
    if expiry_days:
        try:
            expires = datetime.now() + timedelta(days=int(expiry_days))
        except ValueError:
            flash('Термін дії має бути числом.', 'warning')
            pass 

    resp.set_cookie(key, value, expires=expires)
    flash(f'Кукі "{key}" успішно додано.', 'success')
    return resp

@users_bp.route('/delete-cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
        
    key_to_delete = request.form.get('key')
    resp = make_response(redirect(url_for('users.profile')))
    
    if key_to_delete:
        
        if key_to_delete in request.cookies:
            resp.delete_cookie(key_to_delete)
            flash(f'Кукі "{key_to_delete}" видалено.', 'success')
        else:
            flash(f'Кукі "{key_to_delete}" не знайдено.', 'warning')
    else:
        
        for key in request.cookies:
            if key not in ['session', 'theme']: 
                resp.delete_cookie(key)
        flash('Всі кастомні кукі видалено.', 'success')
        
    return resp



@users_bp.route('/set-theme')
def set_theme():
    theme = request.args.get('theme', 'light') 
    if theme not in ['light', 'dark']:
        theme = 'light'
        
    resp = make_response(redirect(url_for('users.profile')))
    
    
    resp.set_cookie('theme', theme, max_age=30*24*60*60) 
    flash(f'Тему змінено на "{theme}".', 'info')
    return resp