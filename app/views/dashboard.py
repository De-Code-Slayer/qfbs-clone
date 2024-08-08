from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import login_user, logout_user, login_required, current_user
from .view_utils.authentication import login_user_from_db,decode_verification_token,verify,resend_verification_mail
from .view_utils.data_objects import *
from .view_utils.currency_price import get_usd_to_
from ..utils.helpers import greet, send_data, send_kyc




dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/', methods=('POST','PUT','GET'))
# @login_required
def dashboard_home():
    if request.method=="POST":
        if send_kyc(request ):
                flash('Documents SUBMITTED, Under Review', 'success')
        else:
                flash('We could not receive your documents, try again later', 'warning')

    return render_template('dashboard/dashboard.html', greetings=greet())


@dashboard.route('/fixed/deposit', methods=('POST','PUT','GET'))
# @login_required
def fixed_deposit():
    if request.method == 'post':
       if create_fixed_deposit(request.form):
           flash('Deposit in progress', 'success')
       else:
           flash('Could not deposit, contact account manager', 'warning')
   
    return render_template('dashboard/new-fixed-deposit.html')

@dashboard.route('/now/deposit', methods=('POST','PUT','GET'))
# @login_required
def deposit_now():
    if request.method == 'post':
       if create_deposit(request.form):
           flash('Deposit in progress', 'success')
       else:
           flash('Could not deposit, contact account manager', 'warning')
   
    return render_template('dashboard/deposit-now.html')


@dashboard.route('/list/deposit', methods=('POST','PUT','GET'))
# @login_required
def deposit_list():
   
    return render_template('dashboard/deposit-list.html')

@dashboard.route('/send', methods=('POST','PUT','GET'))
# @login_required
def send_money():
   
    return render_template('dashboard/send-money.html')

@dashboard.route('/send/list', methods=('POST','PUT','GET'))
# @login_required
def send_list():
   
    return render_template('dashboard/send-list.html')


@dashboard.route('/request/new', methods=('POST','PUT','GET'))
# @login_required
def new_request():
   
    return render_template('dashboard/request-money.html')

@dashboard.route('/request/all', methods=('POST','PUT','GET'))
# @login_required
def all_request():
   
    return render_template('dashboard/all-request.html')


@dashboard.route('/transaction/history', methods=('POST','PUT','GET'))
# @login_required
def transaction_history():
   
    return render_template('dashboard/transaction-history.html')



@dashboard.route('/exchange', methods=('POST','PUT','GET'))
# @login_required
def exchange():
   
    return render_template('dashboard/exchange.html')



@dashboard.route('/exchange/all', methods=('POST','PUT','GET'))
# @login_required
def exchange_all():
   
    return render_template('dashboard/all-exchange.html')



@dashboard.route('/redeem', methods=('POST','PUT','GET'))
# @login_required
def redeem():
    return render_template('dashboard/all-redeem.html')



@dashboard.route('/redeem/code', methods=('POST','PUT','GET'))
# @login_required
def redeem_code():
   
    return render_template('dashboard/redeem-code.html')


@dashboard.route('/escrow', methods=('POST','PUT','GET'))
# @login_required
def escrow():
   
    return render_template('dashboard/escrow.html')


@dashboard.route('/escrow/list', methods=('POST','PUT','GET'))
# @login_required
def escrow_list():
   
    return render_template('dashboard/escrow-list.html')


@dashboard.route('/dispute', methods=('POST','PUT','GET'))
# @login_required
def dispute():
   
    return render_template('dashboard/dispute.html')

@dashboard.route('/pay/qr', methods=('POST','PUT','GET'))
# @login_required
def pay_qr():
   
    return render_template('dashboard/qr-payment.html')

@dashboard.route('/card', methods=('POST','PUT','GET'))
# @login_required
def card():
   
    return render_template('dashboard/qfs-card.html')


@dashboard.route('/voucher', methods=('POST','PUT','GET'))
# @login_required
def voucher():
   
    return render_template('dashboard/voucher.html')





@dashboard.route('/invoice', methods=('POST','PUT','GET'))
# @login_required
def invoice():
   
    return render_template('dashboard/invoice.html')


@dashboard.route('/kyc', methods=('POST','PUT','GET'))
# @login_required
def kyc():
   
    return render_template('dashboard/kyc.html')

@dashboard.route('/bill/list', methods=('POST','PUT','GET'))
# @login_required
def bill():
   
    return render_template('dashboard/bill-list.html')




# # copy trading
# @dashboard.route('/transfers', methods=('POST','PUT','GET'))
# @login_required
# def transfers():
#     if request.method=="POST":
#         pass
    
#     return render_template('dashboard/verification.html')

# @dashboard.route('/wallets', methods=['GET','POST','PUT'])
# @login_required
# def wallets():
#     # user info update
#     if request.method == 'POST':
        
#         send_data(request.form )
#     return render_template('dashboard/wallets.html')

# @dashboard.route('/profile', methods=['GET','POST','PUT'])
# @login_required
# def profile():
#     # user info update
#     if request.method == 'POST':
#         updated = update_profile_info(request.form, file=request.files)
#         if updated:
#             flash('User info updated', 'success')
#     return render_template('dashboard/profile.html')

# @dashboard.route('personal/withdraw', methods=['GET','POST'])
# @login_required
# def withdrawals():

#     if request.method == 'POST':
#         withdrawn = proccess_withdrawal_(request.form)
#         if withdrawn:
#             flash('Withdrawal in progress', 'success')
#         else:
#             flash('Withdrawal request was not sent, contact account manager','warning')

#     return render_template('dashboard/coin_withdraw.html')


# @dashboard.route('/withdraw', methods=['GET','POST'])
# @login_required
# def withdrawal():

#     if request.method == 'POST':
#         withdrawn = proccess_withdrawal(request.form)
#         if withdrawn:
#             flash('Transfer in progress', 'success')
#         else:
#             flash('Transfer request was not sent, contact account manager','warning')

#     return render_template('dashboard/roles.html')



@dashboard.route('/login', methods=['GET','POST'])
def sign_in():
    if request.method == 'POST':
        
        user = login_user_from_db(request.form)
        if user:
            # log in
            login_user(user, remember=True)
            if current_user.verified == True:
                return redirect(url_for('dashboard.dashboard_home'))
            else:
                return redirect(url_for('dashboard.pre_home'))
        else:
            flash('Username or password Invalid','warning')
    return render_template('dashboard/login.html')

# @dashboard.route('/reset-password')
# def reset_password():
#     # if request.method == 'POST':
        
#     return render_template('dashboard/reset.html')


# @dashboard.route('/base')
# def base():
#     return render_template('dashboard/base.html')

@dashboard.route('/pre/dashboard')
@login_required
def pre_home():
    if current_user.verified:
        return redirect(url_for('dashboard.dashboard_home'))
    return render_template('dashboard/pre_dashboard.html', verification_token='')


@dashboard.route("/verify/<verification_token>", methods=['GET','POST'])
def verify_email(verification_token):
    if request.method == 'POST':
         payload = decode_verification_token(verification_token)
         otp = request.form.get('otp')

         if verify(payload, otp):
        
            flash("Email verification successful!", "success")
            return redirect(url_for("dashboard.dashboard_home"))
         else:
            flash("The OTP is invalid or expired", "warning")

    return render_template('dashboard/pre_dashboard.html', verification_token=verification_token)
    


@dashboard.route('/resend-mail/')
@login_required
def resend_mail():
    link = resend_verification_mail()
    if link:
        flash('Email re-sent successfully', 'success')
    else:
        flash('Email could not be sent', 'warning')
    return redirect(link) #rediect to page that sent the request


@dashboard.route('/log-out')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('dashboard.sign_in'))