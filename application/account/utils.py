from flask import url_for, current_app
from flask_mail import Message
from application import mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

""" ---------- E M A I L  R E S E T ------------------------------------------------------------------------------------------ """
# Serializer uses the apps SECRET_KEY to encide whatever criteria is returned in the 's.dumps' statement.
# Deciding is done in the 'verify_reset_token(token)' function via 's.loads(token)[<criteria>]
def get_reset_token(user_id, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': user_id}).decode('utf-8')


def send_reset_email(user_id, email):
    # Create token for the user
    token = get_reset_token(user_id)

    # Condifgure the subject, sender, and recipient/s
    msg = Message('Budget Buddy Password Reset', sender='mhart1992@gmail.com', recipients=[email])
    # Configure the body and pass the token parameter, as well as _external=True to tell python it's an external link
    msg.body = f'''Please use the link below to reset your Budget Buddy password.
    {url_for('account.reset_token', token=token, _external=True)}

    If you did not request a password change, simply ignore this email and no changes will be made.
    '''

    mail.send(msg)


def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    
    return user_id