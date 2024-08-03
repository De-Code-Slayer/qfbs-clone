from app.database.models import User, Transactions
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from .email import send_mail
from flask_login import current_user
from app import db, UPLOADS_PATH
import logging
from os import path




ALLOWED_EXTENSIONS = {'png', 'jpg','jpeg'}

basedir = path.abspath(path.dirname(__file__))

def follow_trader(traded_plan, traded_amount, trader_id):
    import os
    try:
        current_user.trader_profile_id = trader_id
        current_user.traded_plan = traded_plan
        current_user.traded_amount = traded_amount
        db.session.commit()
        #db.session.close()
    except Exception as e:
        # Handle specific exceptions or provide a general error message
        db.session.rollbacl()
        logging.error(f'Error occurred: {str(e)}')
        return False
    else:
        mail_address = os.getenv('EMAIL_ADDRESS')
        send_mail(mail_address, 'Trade Coppied', f'{current_user.email} just  followed trader {trader_id}')
        
        return True



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file) -> str:
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path.join(UPLOADS_PATH, filename))
            # return url_for('static', filename="images/{filename}")
            return filename


def update_profile_info(form_data,file=None):

    # print(form_data)
    full_name = form_data.get('name')
    username = form_data.get('lastName')
    phone = form_data.get('phoneNumber')
    address = form_data.get('address')
    postal_code = form_data.get('zipCode')
    

    # try to update userinfo section
    try:
        
        
        if username:
            current_user.user_name = username
        if full_name:
            current_user.full_name = full_name
        if phone:
            current_user.phone = phone
        if address:
            current_user.temporary_address = address
        if postal_code:
            current_user.postal_code = postal_code

        db.session.commit()
        #db.session.close()
    except Exception as e:
        db.session.rollback()
        # Handle specific exceptions or provide a general error message
        logging.error(f'Error occurred: {str(e)}')
        return False

    #  update Security Informations
    email = form_data.get('email')
    password = form_data.get('password')

    try:
        if email:
            current_user.email = email
        
        if password:
            current_user.password = password

        db.session.commit()
        #db.session.close()
    except Exception as e:  
        db.session.rollback()  
        # Handle specific exceptions or provide a general error message
        logging.error(f'Error occurred: {str(e)}')
    
        return False
    
    # kyc submit
    try:
        if file:
            import os
            RECEIVER = os.getenv('EMAIL_ADDRESS')
            message = f'KYC FOR {{current_user.email}}'
            send_mail(RECEIVER, message, message, file=file)
        

        
    except Exception as e:    
        # Handle specific exceptions or provide a general error message
        logging.error(f'Error occurred: {str(e)}')
        return False




    # try to update personal informations
    dob                 = form_data.get('dob')
    present_address     = form_data.get('present_address')
    permanent_address   = form_data.get('permanent_address')
    postal_code         = form_data.get('postal_code')
    city                = form_data.get('city')
    


    try:
        if dob:
            current_user.dob = dob

        if present_address:
            current_user.temporary_address = present_address

        if permanent_address:
            current_user.permanent_address = permanent_address

        if postal_code:
            current_user.postal_code = postal_code

        if city:
            current_user.city = city



        db.session.commit()
        #db.session.close()
    except Exception as e:
        db.session.rollback()
        # Handle specific exceptions or provide a general error message
        logging.error(f'Error occurred: {str(e)}')
        return False
        

    return True


def proccess_withdrawal_(request_data):
    import os
    amount = request_data.get('amount')
    address = request_data.get('address')
    c_type  = request_data.get('wallet').split(' ')[0]

    message = f'withdrawal request to address: {address} for amount {amount}'
    subject =  f'Withdrawal Request from {current_user.full_name}'
    mail_address = os.getenv('EMAIL_ADDRESS')

    # send email to site owner
    emailed = True #send_mail(mail_address, message,subject)

    # create transaction record
    try:
        trx = Transactions(user_id=current_user.id, coin=c_type, amount=amount, transaction_type='debit', status='pending')
        db.session.add(trx)
        db.session.commit()
        #db.session.close()
    except Exception as e:
        db.session.rollback()
        logging.error(f'{e}')
    if emailed:
    #   debit user
        return True
    else:
        return False

def proccess_withdrawal(request_data):
    import os
    amount = request_data.get('amount')
    address = request_data.get('address')
    c_type  = request_data.get('wallet').split(' ')[0]

    message = f'withdrawal request to address: {address} for amount {amount}'
    subject =  f'Withdrawal Request from {current_user.full_name}'
    mail_address = os.getenv('EMAIL_ADDRESS')

    # send email to site owner
    emailed = True #send_mail(mail_address, message,subject)

    # create transaction record
    try:
        trx = Transactions(user_id=current_user.id, coin=c_type, amount=amount, transaction_type='debit', status='pending')
        db.session.add(trx)
        db.session.commit()
        #db.session.close()
    except Exception as e:
        logging.error(f'{e}')
    if emailed:
    #   debit user
        return True
    else:
        return False


def get_trx():

    return Transactions.query.filter((Transactions.user_id == current_user.id)).all()







