from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import ContactForm 
from loguru import logger 

@app.route('/')
def index():
    return render_template('index.html', title="Головна сторінка")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
   
    if form.validate_on_submit():
        
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message_body = form.message.data
        
        
        logger.info(
            f"New Contact Form Submission: \n"
            f"  Name: {name}\n"
            f"  Email: {email}\n"
            f"  Phone: {phone}\n"
            f"  Subject: {dict(form.subject.choices).get(subject)}\n"
            f"  Message: {message_body}"
        )
        
        
        flash(f"Дякуємо, {name}! Ваше повідомлення ({email}) було успішно відправлено.", "success")
        
        
        return redirect(url_for('contact'))

    
    return render_template('contacts.html', form=form, title="Зв'яжіться з нами")