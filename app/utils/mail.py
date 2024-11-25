# from itsdangerous import URLSafeTimedSerializer
# from . import app
import os
import logging




EMAIL_ADDRESS  = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SENDER_ADDRES  = os.environ.get('SENDER_ADDRES')







# def generate_confirmation_token(email):
#     serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


# def confirm_token(token, expiration=3600):
#     serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     try:
#         email = serializer.loads(
#             token,
#             salt=app.config['SECURITY_PASSWORD_SALT'],
#             max_age=expiration
#         )
#     except:
#         return False
#     return email











def smtpmailer(receiver, message, subject, file=None, mail_type='html'):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    # create email obj
    msg = MIMEMultipart()
    msg['From'] = 'QFBS <info@quantumfinancialsystem.support>'
    msg['To'] = receiver
    msg['Subject'] = subject

    # add the message body
    msg.attach(MIMEText(message, mail_type))

    if file:
      for filex in file:
        # Use the file's stream from Flask's FileStorage
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(filex.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename=filex.filename  # Use the original filename
        )
        msg.attach(attachment)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    try:

    
    # Authentication
      s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
      # sending the mail
      s.sendmail(SENDER_ADDRES, receiver, msg.as_string())
    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.error('An error occurred while sending the email: %s', str(e))
        return False
    finally:
        # terminating the session
        s.quit()
    return True



    


# print(smtpmailer('pablothebmp@gmail.com','This is a test mail','Test Mail'))





