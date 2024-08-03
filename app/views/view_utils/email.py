from ...utils.mail import smtpmailer 
def send_mail(address, message, subject,file=None) -> bool:
    return smtpmailer(address,message,subject,file=file)
    
