from app.database.models import User, Referrals, BTC,USDT,ETH,SOL,RIPPLE,ALGO,XDC,STELLAR
from flask import (session, url_for, flash)
from app import db
import logging
from .email import send_mail
import jwt
import datetime
import os

WEBSITE_URL = os.getenv('WEBSITE_URL')

def login_user_from_db(form_data) -> User:
    try:
    # Extract the required data from form_data using argument unpacking
        email, password,  = (    
            form_data.get('email'),
            form_data.get('password')
        )
        # ... extract other necessary fields
        
        # return user from db
        return User.query.filter((User.email == email) & (User.password == password)|(User.user_name == email) & (User.password == password)).first()

    except Exception as e:
        # Handle specific exceptions or provide a general error message
        logging.error(f'Error occurred during user registration: {str(e)}')
        return False
    

def get_user_by_email(email):
    return User.query.filter((User.email == email)).first()

def check_if_user_exists_in_db(email):
    return User.query.filter(User.email == email).first()

def handle_registration(form_data):
    from flask import render_template
    try:
    # Extract the required data from form_data using argument unpacking
        full_name, email, username, password, country, phone_code, phone, postal_code, referer, sex, dob = (
            form_data.get('name',''),
            form_data.get('email',''),
            form_data.get('username',''),
            form_data.get('password',''),
            form_data.get('country',''),
            form_data.get('phone_code',''),
            form_data.get('phone',''),
            form_data.get('postal_code',''),
            form_data.get('referee',''),
            form_data.get('sex',''),
            form_data.get('dob','')

        )
        # ... extract other necessary fields
        
        # check if user already exists
        if check_if_user_exists_in_db(email):
            logging.error(f'User already exists')
            return {'error': 'User already exists'}

        
        
        user = User(
            full_name=full_name,
            email=email,
            sex=sex,
            dob=dob,
            password=password,
            user_name=username,
            country=country,
            phone=phone,
            phone_code=phone_code,
            username=username,
            postal_code=postal_code,
        )
        # email_link = f'{WEBSITE_URL}/dashboard/verify/{generate_verification_token(email)}'
        email_link = url_for('dashboard.verify_email', verification_token=generate_verification_token(email))


        if referer and Referrals.query.filter(Referrals.reffered_user_name == referer).first():
            try:
            #   crte referals
              referal = Referrals(reffered_user_name=full_name, username=referer)
              
              db.session.add(referal)
              
            except Exception as e:
                print(f'==============={e}===================')
                pass
        # elif session.get('referral_code', None):
        #     referer = session.get('referral_code', None)  # Get the referral code from the session (if available) to mark the referrer
        #     referal = Referrals(reffered_user_name=full_name, username=referer)
        #     db.session.add(referal)



        # Save the user to the database
        db.session.add(user)
        try:
            db.session.commit()
            #db.session.close()
        except Exception as e:
            db.session.rollback()

            print(f'==========={form_data}===========')
            print(f'==========={e}===========')
            return 'USERNAME OR EMAIL EXIST'

        html_mail = render_template('email/confirmemail.html', email_link=email_link)
        print(html_mail)
        # send_mail(email, html_mail,'Verify Email' )

    except Exception as e:
        # Handle specific exceptions or provide a general error message
        logging.error(f'Error occurred during user registration: {str(e)}')
        return False
    
    # Return a response indicating successful registration

    
    return email_link

def resend_verification_mail():
    from flask_login import current_user
    from flask import render_template
    email_link = f'{WEBSITE_URL}/dashboard/verify/{generate_verification_token(current_user.email)}'

    html_mail = render_template('email/confirmemail.html', email_link=email_link)
    
    # send_mail(current_user.email,html_mail,'Verify Email' )
    return email_link



def verify(payload, otp):
    from flask_login import current_user
    if "user_id" in payload :
        user_id = payload["user_id"]
        user = get_user_by_email(user_id)

        if user and current_user.id == user.id:
            # Check if the token is not expired
            # Assuming payload["exp"] is a Unix timestamp (an integer)
            timestamp = payload["exp"]
            code = payload['code']
            exp_datetime = datetime.datetime.utcfromtimestamp(timestamp)

            if exp_datetime >= datetime.datetime.utcnow() and code == otp:
                # Update the 'update' column to true
                user.verified = True
            try:
                db.session.commit()
                #db.session.close()
            except Exception as e:
                db.session.rollback()
                print(f'==========={e}===========')
            return True
            
        return False
            
SECRET_KEY = os.getenv('SECRET_KEY') 
EXPIRATION_TIME = os.getenv('EXPIRATION_TIME')  # Set the expiration time in seconds (e.g., x hours)



def generate_verification_token(user_id):
    import random
    choice = [0,1,2,3,4,5,6,7,8,9]
    payload = {
        "user_id": user_id,
        'code': f'{random.choice(choice)}{random.choice(choice)}{random.choice(choice)}{random.choice(choice)}' ,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(EXPIRATION_TIME))
    }
    print(payload)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_verification_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None

def create_coins(current_user):
    # create coins
        btc = BTC(coin='Bitcoin', user_id=current_user.id, coin_short='BTC')
        usdt = USDT(coin='USDT', user_id=current_user.id, coin_short='USDT')
        eth = ETH(coin='Ethereum', user_id=current_user.id, coin_short='ETH')
        sol = SOL(coin='Solana', user_id=current_user.id, coin_short='SOL')
        algo = ALGO(coin='Algorand', user_id=current_user.id, coin_short='A')
        ripple = RIPPLE(coin='Ripple', user_id=current_user.id, coin_short='Ripple')
        xdc = XDC(coin='XDC', user_id=current_user.id, coin_short='XDC')
        stellar = STELLAR(coin='Stellar', user_id=current_user.id, coin_short='Stellar')


        try:
            db.session.add(btc)
            db.session.add(eth)
            db.session.add(usdt)
            db.session.add(sol)
            db.session.add(ripple)
            db.session.add(algo)
            db.session.add(xdc)
            db.session.add(stellar)
            db.session.commit()
            #db.session.close()
        except Exception as e:
            db.session.rollback()
            print(f'==========={e}===========')



def send_reset(form_data):
    from flask import render_template

    email = form_data.get('email')

    if not get_user_by_email(email):
        flash('user not found', 'warning')
        return False
    
    # Generate a JWT token
    reset_token = jwt.encode({
        'sub': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }, os.getenv('SECRET_KEY'), algorithm='HS256')

    # Create the reset email
    reset_url = f'{WEBSITE_URL}/password/{reset_token}'  # Adjust URL to your application
    print(reset_url)
    
    html_mail = render_template('email/reset.html', email_link=reset_url)
    
    if send_mail(email, html_mail, 'Reset Password' ):
        flash('Email sent success','success')
    else:
        flash('Could not send mail','warning')
        

def verify_reset(form_data, token):
    pass