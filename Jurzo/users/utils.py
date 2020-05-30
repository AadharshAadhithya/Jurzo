from flask_mail import Message
from Jurzo import mail
from flask import url_for


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@jurzo.com',
                  recipients=[user.email])
    msg.body = '''To reset Your Password, visit the following link:
{}

    If you did not make the request , Please Ignore the email

    '''.format(url_for('users.reset_token', token=token, _external=True))
    mail.send(msg)
