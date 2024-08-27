from app.database.models import User, Transactions
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from .email import send_mail
from flask_login import current_user
from flask import flash
from app import db, UPLOADS_PATH
import logging
from os import path
from ...database.models import *




ALLOWED_EXTENSIONS = {'png', 'jpg','jpeg'}

basedir = path.abspath(path.dirname(__file__))



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
    email = request_data.get('recipient')
    currency  = request_data.get('currency')
    note  = request_data.get('note')
    wallet = request_data.get('methodId')

    message = f'Request money to address: {email} for amount {amount}'
    subject =  f'Request from {current_user.full_name}'
    mail_address = os.getenv('EMAIL_ADDRESS')

    # send email to site owner
    emailed = True #send_mail(mail_address, message,subject)

    # create transaction record
    try:
        trx = RequestMoney(user_id=current_user.id,wallet=wallet, note=note, currency=currency, amount=amount, type='money request', status='pending')
        db.session.add(trx)
        db.session.commit()
        #db.session.close()
    except Exception as e:
        db.session.rollback()
        logging.error(f'{e}')
        return False

    # create transaction record
    try:
        trx = Transactions(user_id=current_user.id, coin=currency, amount=amount, transaction_type='debit', status='pending')
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

def proccess_withdrawal(request_data):
    import os
    amount = float(request_data.get('amount'))
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

def get_exchange_rate(from_currency, to_currency):
        # Fetch or calculate the exchange rate here
        # For the sake of example, we'll use a static dictionary
        exchange_rates = {
            ('USD', 'BTC'): 0.000065, # Example rates
            ('BTC', 'USD'): 15385.00,
            # Add more rates as needed
        }
        return exchange_rates.get((from_currency, to_currency), 1.0)

def calculate_gas_fee(amount):
        # For example, a fixed fee or percentage of the amount
        # fee_percentage = current_user.gas_fee  
        fee_percentage = 0.01  # 1% fee
        return amount * fee_percentage


def exchange_curr(request_data):

      # create exchange request
    amount = float(request_data.get('amount'))
    _from_wallet = request_data.get('from_wallet')
    _to_wallet  = request_data.get('to_wallet')


    # automate Exchange
    # Map wallet codes to model classes
    wallet_classes = {
        'BTC': BTC,
        'SOL': SOL,
        'ETH': ETH,
        'XRP': RIPPLE,
        'USD': USDT,
        'ALGO': ALGO,
        'XLM': STELLAR,
        'XDC': XDC,
        'MATIC': POLY
    }

    from_wallet_class = wallet_classes[_from_wallet]
    to_wallet_class = wallet_classes[_to_wallet]

  
    try:
        # Retrieve wallet records
       # Retrieve wallet records for the current user
        from_wallet = from_wallet_class.query.filter_by(user_id=current_user.id).first()
        to_wallet = to_wallet_class.query.filter_by(user_id=current_user.id).first()

        # Calculate exchange rate and gas fee
        exchange_rate = get_exchange_rate(_from_wallet, _to_wallet)
        gas_fee = calculate_gas_fee(amount)

        # Calculate the amount to be deducted from the source wallet
        total_amount_deducted = amount + gas_fee

        if from_wallet == to_wallet:
            flash('Cannot exchange between same wallets', 'warning')
            return False 

        # Calculate the amount to be added to the destination wallet
        amount_received = amount / exchange_rate

        if not from_wallet or not to_wallet:
            flash('wallet not found', 'danger')
            return False 

        if float(from_wallet.amount) < total_amount_deducted:
            flash('Insufficient funds', 'warning')
            return False

        # Deduct amount from the source wallet
        from_wallet.amount -= total_amount_deducted
        # Add amount to the destination wallet
        to_wallet.amount += amount_received

        # Commit changes to the database
        
        flash('Exchange successful', 'success')
       

    except Exception as e:
        db.session.rollback()
        logging.error(f'{e}')

    # create transaction record

    try:
        trx = Exchange(user_id=current_user.id, from_wallet=_from_wallet, to_wallet=_to_wallet, amount=amount, status='success')
        db.session.add(trx)
        #db.session.close()
    except Exception as e:
        db.session.rollback()
        logging.error(f'{e}')

      # create trx history
    try:
        trx = Transactions(user_id=current_user.id, currency=_from_wallet, amount=amount, transaction_type='exchange', status='success')
        db.session.add(trx)
        db.session.commit()
        #db.session.close()
    except Exception as e:
        db.session.rollback()
        logging.error(f'{e}')
    return True

def create_tranx_rec(c_type, amount , ):
    # create transaction record
    try:
        trx = Transactions(user_id=current_user.id, coin=c_type, amount=amount, transaction_type='debit', status='pending')
        db.session.add(trx)
        db.session.commit()
        #db.session.close()
    except Exception as e:
        logging.error(f'{e}')

def get_trx():

    # return Transactions.query.filter((Transactions.user_id == current_user.id)).all()
    return format_combined_transactions()


def create_fixed_deposit(form_data):
    plan  = form_data.get('plan')
    interest  = form_data.get('currency')
    min_amount  = form_data.get('min')
    max_amount  =  form_data.get('max')
    tenure  =  form_data.get('tenure')
    amount  =  form_data.get('amount')

    try:
         new_trx = Fixed_DepositTRX(plan=plan, interest=interest, min_amount=min_amount, max_amount=max_amount, tenure=tenure,amount=amount)
         db.session.add(new_trx)
         db.session.commit()
    except Exception as e:
        logging.error(f'{e}')
        return False
    return True

    


def create_deposit(form_data):
    curency  = form_data.get('currency')
    amount  = form_data.get('amount')
    wallet  = form_data.get('methodId')
    

    try:
         new_trx = DepositTRX(curency=curency, wallet=wallet,amount=amount, user_id = current_user.id)
         db.session.add(new_trx)
         db.session.commit()
    except Exception as e:
        logging.error(f'{e}')
        return False
    return True

def send_money_(form_data):
    recepient_email = form_data.get('recipient')
    currency = form_data.get('currency')
    amount = form_data.get('amount')
    note = form_data.get('note')
    charge_recepient = True if form_data.get('charge_from') == 1 else False

    try:
         new_trx = SendMoney(currency=currency, recepient_email=recepient_email,amount=amount, note=note, charge_recepient=charge_recepient, user_id = current_user.id)
         db.session.add(new_trx)
         db.session.commit()
    except Exception as e:
        logging.error(f'{e}')
        return False
    return True
    
def get_transfers(form_data=None):

      # Start with the base query for transfers of the current user
    query = SendMoney.query.filter(SendMoney.user_id == current_user.id)

        # Check if form_data is provided and apply filters
    if form_data:
        tr_id = form_data.get('utr')
        sender = form_data.get('sender')
        currency = form_data.get('currency_id')
        email = form_data.get('email')
        date = form_data.get('created_at')
        type_ = form_data.get('type')
        status = form_data.get('status')
        min_amount_str = form_data.get('min')
        max_amount_str = form_data.get('max')
        
        # Convert dates from string to datetime objects, if provided
        start_date = datetime.strptime(date, '%Y-%m-%d') if date else None
        
        
        # Convert amounts to floats, if provided
        min_amount = float(min_amount_str) if min_amount_str else None
        max_amount = float(max_amount_str) if max_amount_str else None
        
        # Apply filters
        if tr_id:
            query = query.filter(SendMoney.id == tr_id)
        
        if email:
            query = query.filter(SendMoney.recepient_email.ilike(f'%{email}%'))
        
        if start_date:
            query = query.filter(SendMoney.date == start_date)
        
        if min_amount is not None:
            query = query.filter(SendMoney.amount >= min_amount)
        
        if type_ is not None:
            query = query.filter(SendMoney.type == type_)

        if status is not None:
            query = query.filter(SendMoney.status == status)

        if currency is not None:
            query = query.filter(SendMoney.currency == currency)

        if sender is not None:
            query = query.filter(SendMoney.user_id == sender)
            
        if max_amount is not None:
            query = query.filter(SendMoney.amount <= max_amount)
    
    # Fetch and return the results
    return query.all()


def create_request_money(form_data):
        recepient_email = form_data.get('wallet')
        currency = form_data.get('wallet')
        amount = form_data.get('wallet')
        note = form_data.get('wallet')
       

        try:
         new_trx = RequestMoney(currency=currency, recepient_email=recepient_email,amount=amount, note=note)
         db.session.add(new_trx)
         db.session.commit()
        except Exception as e:
             logging.error(f'{e}')
             return False
        return True


def create_exchange(form_data):
    from_wallet = form_data.get('wallet')
    to_wallet = form_data.get('wallet')
    amount = form_data.get('wallet')

    try:
         new_trx = Exchange(from_wallet=from_wallet, to_wallet=to_wallet,amount=amount)
         db.session.add(new_trx)
         db.session.commit()
    except Exception as e:
        logging.error(f'{e}')
        return False
    return True


def create_redeem_code(form_data):
    pass

def verify_redeem_code(form_data):
    pass

def create_escrow(form_data):
    recepient_email = form_data.get('wallet')
    currency = form_data.get('wallet')
    amount = form_data.get('wallet')
    note = form_data.get('wallet')
    charge_recepient = form_data.get('wallet')

    try:
         new_trx = Escrow(currency=currency, recepient_email=recepient_email,amount=amount, note=note, charge_recepient=charge_recepient)
         db.session.add(new_trx)
         db.session.commit()
    except Exception as e:
        logging.error(f'{e}')
        return False
    return True


def create_dispute(form_data):
    pass

def create_voucher(form_data):
    pass


def create_invoice(form_data):
    pass


def create_bill(form_data):
    pass


def create_payout(form_data):
    pass


def create_qrpayment(form_data):
    pass

def create_qfs_card(form_data):
    pass





def query_combined_transactions():
    from sqlalchemy import literal
    # Query each table and add a source_table column
    transactions = db.session.query(
        Transactions.id,
        Transactions.amount,
        Transactions.timestamp.label('date'),
        literal('transactions').label('source_table')
    ).all()

    fixed_deposit_trx = db.session.query(
        Fixed_DepositTRX.id,
        Fixed_DepositTRX.amount,
        Fixed_DepositTRX.date.label('date'),
        literal('fixed_deposit_trx').label('source_table')
    ).all()

    deposit_trx = db.session.query(
        DepositTRX.id,
        DepositTRX.amount,
        DepositTRX.date.label('date'),
        literal('deposit_trx').label('source_table')
    ).all()

    send_money = db.session.query(
        SendMoney.id,
        SendMoney.amount,
        SendMoney.date.label('date'),
        literal('send_money').label('source_table')
    ).all()

    request_money = db.session.query(
        RequestMoney.id,
        RequestMoney.amount,
        RequestMoney.date.label('date'),
        literal('request_money').label('source_table')
    ).all()

    exchange = db.session.query(
        Exchange.id,
        Exchange.amount,
        Exchange.timestamp.label('date'),
        literal('exchange').label('source_table')
    ).all()

    # Combine all results into one list
    combined = (
        transactions + 
        fixed_deposit_trx + 
        deposit_trx + 
        send_money + 
        request_money + 
        exchange
    )

    # Sort combined results by date in descending order
    sorted_combined = sorted(combined, key=lambda x: x.date, reverse=True)

    return sorted_combined

# Convert results to a list of dictionaries for easier display or further processing
def format_combined_transactions():
    combined_transactions = query_combined_transactions()
    formatted_transactions = [
        {
            'id': record.id,
            'amount': record.amount,
            'date': record.date,
            'type': record.source_table,
        }
        for record in combined_transactions
    ]
    return formatted_transactions

# # Example usage
# formatted_transactions = format_combined_transactions()
# for transaction in formatted_transactions:
#     print(transaction)







