from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import login_user, logout_user, login_required, current_user
from .view_utils.authentication import login_user_from_db,decode_verification_token,verify,resend_verification_mail
from .view_utils.data_objects import update_profile_info, follow_trader, proccess_withdrawal,proccess_withdrawal_,get_trx
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

    return render_template('dashboard/dashboard.html', greetings=greet(), trx=get_trx())

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



# @dashboard.route('/login', methods=['GET','POST'])
# def sign_in():
#     if request.method == 'POST':
        
#         user = login_user_from_db(request.form)
#         if user:
#             # log in
#             login_user(user, remember=True)
#             if current_user.verified == True:
#                 return redirect(url_for('dashboard.dashboard_home'))
#             else:
#                 return redirect(url_for('dashboard.pre_home'))
#         else:
#             flash('Username or password Invalid','warning')
#     return render_template('dashboard/login.html')

# @dashboard.route('/reset-password')
# def reset_password():
#     # if request.method == 'POST':
        
#     return render_template('dashboard/reset.html')

# @dashboard.route('/log-out')
# @login_required
# def sign_out():
#     logout_user()
#     return redirect(url_for('dashboard.sign_in'))

# @dashboard.route('/base')
# def base():
#     return render_template('dashboard/base.html')

# @dashboard.route('/pre/dashboard')
# @login_required
# def pre_home():
#     if current_user.verified:
#         return redirect(url_for('dashboard.dashboard_home'))
#     return render_template('dashboard/pre_dashboard.html')


# @dashboard.route("/verify/<verification_token>")
# def verify_email(verification_token):
#     payload = decode_verification_token(verification_token)

#     if verify(payload):
#         flash("Email verification successful!", "success")
#     else:
#         flash("The link is invalid or expired", "warning")


#     return redirect(url_for("dashboard.dashboard_home"))


# @dashboard.route('/resend-mail/')
# @login_required
# def resend_mail():
    if resend_verification_mail():
        flash('Email re-sent successfully', 'success')
    else:
        flash('Email could not be sent', 'warning')
    return redirect(request.referrer or url_for("dashboard.dashboard_home")) #rediect to page that sent the request