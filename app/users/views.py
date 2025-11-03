# --- Старі імпорти ---
from flask import (
    render_template, request, redirect, url_for, flash, session
)
from . import users_bp
from functools import wraps

# --- НОВІ імпорти для кукі ---
from flask import make_response

# --- Старий декоратор @login_required ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Ви повинні увійти, щоб побачити цю сторінку.', 'danger')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Старі маршрути greetings та admin (з Лаб 3) ---
@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age")
    return render_template("users/hi.html", name=name, age=age, title=f"Greetings {name}")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    return redirect(to_url)

# --- Маршрути Завдання 1 (Логін, Вихід) ---
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'user1' and password == '12345':
            session['username'] = username
            flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль. Спробуйте ще раз.', 'danger')
            
    return render_template('users/login.html', title='Логін')

@users_bp.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

# --- Маршрут Завдання 1 + 2 (Профіль, зчитування кукі) ---
@users_bp.route('/profile')
@login_required
def profile():
    # Отримуємо всі кукі з запиту
    cookies = request.cookies
    return render_template('users/profile.html', title='Профіль', cookies=cookies)

# --- Маршрути Завдання 2 (Управління Кукі) ---

@users_bp.route('/add_cookie', methods=['POST'])
@login_required
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    expiry = request.form.get('expiry')

    if not key or not value or not expiry:
        flash('Будь ласка, заповніть всі поля для додавання кукі.', 'warning')
        return redirect(url_for('users.profile'))

    try:
        resp = make_response(redirect(url_for('users.profile')))
        resp.set_cookie(key, value, max_age=int(expiry))
        flash(f'Кукі "{key}" успішно додано!', 'success')
        return resp
    except ValueError:
        flash('Термін дії має бути числом (у секундах).', 'danger')
        return redirect(url_for('users.profile'))

@users_bp.route('/delete_cookie_by_key', methods=['POST'])
@login_required
def delete_cookie_by_key():
    key = request.form.get('key_to_delete')
    
    if not key:
        flash('Будь ласка, вкажіть ключ кукі для видалення.', 'warning')
        return redirect(url_for('users.profile'))

    resp = make_response(redirect(url_for('users.profile')))
    
    if key in request.cookies:
        resp.delete_cookie(key)
        flash(f'Кукі "{key}" видалено.', 'success')
    else:
        flash(f'Кукі з ключем "{key}" не знайдено.', 'warning')
        
    return resp

@users_bp.route('/delete_all_cookies', methods=['POST'])
@login_required
def delete_all_cookies():
    resp = make_response(redirect(url_for('users.profile')))
    
    deleted_count = 0
    for key in request.cookies.keys():
        if key != 'session':
            resp.delete_cookie(key)
            deleted_count += 1
            
    if deleted_count > 0:
        flash(f'Успішно видалено {deleted_count} кукі.', 'success')
    else:
        flash('Не знайдено кукі для видалення (окрім сесії).', 'info')
        
    return resp

# --- НОВИЙ МАРШРУТ (Завдання 3) ---

@users_bp.route('/set_theme/<theme>')
@login_required
def set_theme(theme):
    """Встановлює кукі 'theme' для вибору теми."""
    if theme not in ['light', 'dark']:
        flash('Невідома тема!', 'danger')
        return redirect(url_for('users.profile'))

    # Створюємо відповідь (redirect), щоб додати кукі
    resp = make_response(redirect(url_for('users.profile')))
    
    # Встановлюємо кукі на 1 рік
    # 60 сек * 60 хв * 24 год * 365 днів
    resp.set_cookie('theme', theme, max_age=31536000)
    
    flash(f'Тему змінено на {"темну" if theme == "dark" else "світлу"}.', 'success')
    return resp

