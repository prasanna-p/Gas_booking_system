import os
import secrets
from PIL import Image
from flask_mail import Message
from projectmain import mail
from flask import current_app
from flask import url_for


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pictures', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('Consumer.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and 
    no changes will be made.'''
    mail.send(msg)


def dsend_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('Agent.dreset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and 
    no changes will be made.'''
    mail.send(msg)

def send_email(user,age):
    msg = Message('Gas Booking Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Your request for the Gas has been forwarded to { age.agency_name }.you will be notified when your request is accepted'''
    mail.send(msg)


def send_conformation_email(user,age):
    msg = Message('Gas Booking Confirmation',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Your request for the Gas has been Accepted by { age.agency_name }.the cylinder will be delivered within 3 working days.thank you for your being with Us.'''
    mail.send(msg)
