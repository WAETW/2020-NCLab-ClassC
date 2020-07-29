import smtplib
from email.mime.text import MIMEText

def emergency_mail(sender_email, sender_password, reciver_email, text):

	gmail_user = sender_email
	gmail_password = sender_password
	msg = MIMEText(text)
	msg['Subject'] = 'help'
	msg['From'] = gmail_user
	msg['To'] = reciver_email

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(gmail_user, gmail_password)
	server.send_message(msg)
	server.quit()

	print('Email sent!')
