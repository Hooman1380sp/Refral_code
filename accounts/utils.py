import smtplib
from email.message import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def Send_Otp_Code(*, email, message):
    print(message + "" + email)
    EMAIL_HOST_PASSWORD = "iinzgcwxmsxahzbe"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = "1380hz1380hz@gmail.com"
    EMAIL_PORT_SSL = 465
    msg = EmailMessage()
    msg["Subject"] = "BootCamp Form"
    msg["Form"] = EMAIL_HOST_USER
    msg["To"] = email
    msg.set_content(message)
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT_SSL) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)


def Send_Otp_Code_Forgot_Link(*, to, address="http://127.0.0.1:8000/reset-pass/", random_str):
    print(to)
    print(f"{address}{random_str}/")

    EMAIL_HOST_PASSWORD = "iinzgcwxmsxahzbe"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = "1380hz1380hz@gmail.com"
    EMAIL_PORT_SSL = 465
    msg = EmailMessage()
    msg["Subject"] = "test referral code"
    msg["Form"] = EMAIL_HOST_USER
    # msg["To"] = 'sina.sheykhali.80@gmail.com'
    # msg["To"] = 'alireza.dev1@gmail.com'
    msg["To"] = to
    msg.set_content(f"{address}{random_str}/")
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT_SSL) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)
