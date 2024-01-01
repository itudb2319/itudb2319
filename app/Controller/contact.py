from flask import request, render_template, Blueprint, session, redirect, url_for
from ..Modal.mail_setup import mail, recipient_email
from flask_mail import Message

contactBP = Blueprint('contact', __name__, url_prefix='/contact')

@contactBP.route('/', methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template('contact.html')
    else:
        sender_email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        msg = Message(subject, sender=sender_email, recipients=[recipient_email])
        msg.body = message_body
        mail.send(msg)

        return redirect(url_for('contact.contact'))
