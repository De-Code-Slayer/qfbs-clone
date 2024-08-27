from flask import (
    Blueprint, flash, redirect, render_template, request, url_for,session, send_file
)
from flask_login import current_user, login_user

from .view_utils.authentication import handle_registration, login_user_from_db, create_coins, send_reset, verify_reset


frontend = Blueprint('frontend', __name__, url_prefix='/')



@frontend.route('/')
def home():
    return render_template('landing/index.html')


@frontend.route('/pdf')
def pdf():
    with open('../templates/landing/QFS-GUIDE.pdf','rb') as pdf:    
        return send_file(pdf , attachment_filename='QFS_GUIDE.pdf')

@frontend.route('/index-2')
def home_2():
    return render_template('landing/index-2.html')


@frontend.route('/signup', methods=['GET','POST'])
def register():
    
    if request.method == 'POST':

        form_data = request.form
        registered = handle_registration(form_data)

        if registered == 'USERNAME OR EMAIL EXIST':
            flash('USERMAME ALREADY IN USE', 'warning')

        if registered and registered != {'error': 'User already exists'}:
            # login user
            user = login_user_from_db(form_data)
            login_user(user, remember=True)
            create_coins(current_user)
            # After storing the necessary information, remove the referral code from the session (if present)
            # This ensures that users won't accidentally refer themselves on subsequent registrations
            session.pop('referral_code', None)
            if current_user.verified == True:
                return redirect(url_for('dashboard.dashboard_home'))
            else:
                return redirect(url_for(registered))
        
        elif registered == {'error': 'User already exists'}:
            flash('Email already in use, login instead', 'warning')
            session.pop('referral_code', None)

        else:
            flash('Could not register user', 'warning')
    
    # username = session.get('referral_code', '')
    return render_template('landing/register.html')

@frontend.route('/ref/<referral_code>')
def referral_link(referral_code):
    session['referral_code'] = referral_code
    return redirect(url_for('frontend.register'))


@frontend.route('/reset/password', methods=['POST','GET'])
def forgot_password():
    if request.method == 'POST':
        send_reset(request.form)
    return render_template('landing/reset.html')

@frontend.route('/password/<reset_token>')
def reset_link(reset_token):
    verify_reset(request.form, reset_token)
    
    return render_template('landing/set_password.html')


@frontend.route('/base')
def base():
    import os
    return os.getenv('DATABASE_URL')