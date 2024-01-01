from flask import request, render_template, Blueprint, session, redirect, url_for
from ..Modal.mail_setup import mail, recipient_email
from flask_mail import Message

mailBP = Blueprint('mail', __name__, url_prefix='/contact')

@mailBP.route('/', methods=["GET", "POST"])
def sendMail():
    if request.method == "GET":
        return render_template('mail.html')
    else:
        sender_email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        msg = Message(subject, sender=sender_email, recipients=[recipient_email])
        msg.body = message_body
        mail.send(msg)

        return redirect(url_for('mail.sendMail'))
