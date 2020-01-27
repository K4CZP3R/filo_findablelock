import smtplib, ssl

port = 465
password = "findlock123321"

context = ssl.create_default_context()

plain_message = """\
Subject: Hi there subj

This is sent."""

with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
    server.login("findlockproftaak@gmail.com", password)
    server.sendmail("findlockproftaak@gmail.com", "serewisk@gmail.com", plain_message )
    