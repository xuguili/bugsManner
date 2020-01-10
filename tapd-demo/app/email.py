from flask_mail import Message
from app import mail
from app import app
from threading import Thread

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject,sender,recipients,text_body,text_html):
    msg = Message(subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = text_html
    thread = Thread(target=send_async_email,args=(app,msg))
    thread.start()
