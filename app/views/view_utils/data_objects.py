from app.database.models import User, Transactions, QFSCARD
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
    wallet = request_data.get('wallet_address')

    message = f'Request money from {email} to address: {wallet} for amount {amount}'
    subject =  f'Request from {current_user.full_name}'
    mail_address = os.getenv('EMAIL_ADDRESS')

    # send email to site owner
    emailed = send_mail(mail_address, message,subject)

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
    emailed = send_mail(mail_address, message,subject)

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
        trx = Exchange(user_id=current_user.id, from_wallet=_from_wallet, to_wallet=_to_wallet, charge=gas_fee, exchange_rate=exchange_rate, amount=amount, status='success')
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
         new_trx = Exchange(from_wallet=from_wallet ,to_wallet=to_wallet,amount=amount)
         db.session.add(new_trx)
         db.session.commit()
    except Exception as e:
        logging.error(f'{e}')
        return False
    return True

def generate_redeem_code(currency, amount, note, charge_receiver):
    import hashlib
    import random

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
    wallet = wallet_classes[currency]

    # confirm if amount is available in balance
    currency_wallet = wallet.query.filter_by(user_id=current_user.id).first()
    if currency_wallet.amount < amount:
        flash('Insufficient fund', 'info')
        return False

    # generate code
    unique_string = f"{currency}-{amount}-{note}-{charge_receiver}-{random.randint(1000, 9999)}"
    hash_object = hashlib.sha256(unique_string.encode())
    redeem_code = hash_object.hexdigest()[:12].upper()

    # deduct amount from balance
    currency_wallet.amount -= amount

    # create record in db
    redeem_code_store = {
        'user_id':current_user.id,
        'charge_receiver':charge_receiver,
        'redeem_code': redeem_code,
        'currency': currency,
        'amount': amount,
        'note': note,
        'status': False
    }
    try:
        trx = Transactions(user_id=current_user.id, currency=redeem_code_store['currency'], amount=amount, transaction_type='reedem debit', status='success')
        db.session.add(trx)
        new_redeem = Redeem(**redeem_code_store)
        db.session.add(new_redeem)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'{e}')
        flash('there was an error generating your redeem code, contact support', 'warning')
        return False
    return redeem_code


def create_redeem_code(form_data):
    currency = form_data.get("currency")
    amount = int(form_data.get("amount"))
    note = form_data.get("note")
    charge_receiver = form_data.get("charge_from")

    # create code
    code = generate_redeem_code(currency, amount, note, charge_receiver)
    return code

def verify_redeem_code(form_data):
    redeem_code = form_data.get('redeemCode')
    # Find the redeem code in the database
    redeem_record = Redeem.query.filter_by(redeem_code=redeem_code, status=False).first()
    
    if not redeem_record:
        flash('Invalid or already redeemed code.', 'danger')
        return False

    # Retrieve the wallet class based on the currency
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
    wallet = wallet_classes[redeem_record.currency]

    # Confirm if the current user is the charge receiver
    # if redeem_record.charge_receiver != user_id:
    #     flash('You are not authorized to redeem this code.', 'danger')
    #     return False

    # Update the status of the redeem code to redeemed
    try:
        redeem_record.status = True
        
        
        # Find the receiver's wallet and credit the amount
        receiver_wallet = wallet.query.filter_by(user_id=current_user.id).first()
        if not receiver_wallet:
            flash(' wallet not found for redeem.', 'danger')
            return False
        
        receiver_wallet.amount += redeem_record.amount

        trx = Transactions(user_id=current_user.id, currency=redeem_record.currency, amount=redeem_record.amount, transaction_type='reedem credit', status='success')
        db.session.add(trx)


        db.session.commit()
      

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error redeeming code: {e}')
        flash('There was an error redeeming your code, contact support.', 'warning')
        return False

    flash(f'Redeemed {redeem_record.amount} {redeem_record.currency}. successfully!', 'success')
    return True
    

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
    import os
    _type = form_data.get('type')
    if not current_user.card_requested:
        # send email to site owner for card request
        message = f'{current_user.full_name} has requested for an ATM Card'
        subject =  f'ATM Card Request from {current_user.full_name}'
        mail_address = os.getenv('EMAIL_ADDRESS')

        # get type of card requested
        card_type = _type.upper()
        # generate card details
        card_details = create_card_details(card_type)
        # create card record
        new_card = QFSCARD(**card_details)
        db.session.add(new_card)
        # send email to site owner

        emailed = send_mail(mail_address, message,subject)
        if emailed:
            # current_user.card_requested = True
            db.session.commit()

            flash('Card Created Successfully', 'success')
        else:
            flash('There was a problem completing your card request at the moment, Try again later', 'warning')
            
        return emailed
    flash('Already requested a card', 'info')
    return

def get_medbed():
    return MedBed.query.first()
    
def order_medbed(form_data):
    from ...utils.helpers import send_medbed
    medbed_type = form_data.form.get('category')
    amount = form_data.form.get('amount')
    
    if send_medbed(form_data):
        print(send_medbed(form_data))
        # create order
        new_order = MedBedOrders(user_id=current_user.id, medbed_price=0.00, med_bed=medbed_type, deposit=amount)
        db.session.add(new_order)
        db.session.commit()
        flash('Receipt Submitted, Under verification', 'info')
        return
    
def query_combined_transactions():
    from sqlalchemy import literal
    # Query each table and add a source_table column
    transactions = db.session.query(
        Transactions.id,
        Transactions.amount,
        Transactions.currency.label('currency'),
        Transactions.status.label('status'),
        Transactions.timestamp.label('date'),
        literal('transactions').label('source_table')
    ).filter(Transactions.user_id == current_user.id).all()

    fixed_deposit_trx = db.session.query(
        Fixed_DepositTRX.id,
        Fixed_DepositTRX.amount,
        Fixed_DepositTRX.curency.label('currency'),
        Fixed_DepositTRX.date.label('date'),
        Fixed_DepositTRX.status.label('status'),
        literal('fixed_deposit_trx').label('source_table')
    ).filter(Fixed_DepositTRX.user_id == current_user.id).all()

    deposit_trx = db.session.query(
        DepositTRX.id,
        DepositTRX.amount,
        DepositTRX.curency.label('currency'),
        DepositTRX.date.label('date'),
        DepositTRX.status.label('status'),
        literal('deposit_trx').label('source_table')
    ).filter(DepositTRX.user_id == current_user.id).all()

    send_money = db.session.query(
        SendMoney.id,
        SendMoney.amount,
        SendMoney.currency.label('currency'),
        SendMoney.status.label('status'),
        SendMoney.date.label('date'),
        literal('send_money').label('source_table')
    ).filter(SendMoney.user_id == current_user.id).all()

    request_money = db.session.query(
        RequestMoney.id,
        RequestMoney.amount,
        RequestMoney.currency.label('currency'),
        RequestMoney.status.label('status'),
        RequestMoney.date.label('date'),
        literal('request_money').label('source_table')
    ).filter(RequestMoney.user_id == current_user.id).all()

    exchange = db.session.query(
        Exchange.id,
        Exchange.amount,
        Exchange.to_wallet.label('currency'),
        Exchange.status.label('status'),
        Exchange.timestamp.label('date'),
        literal('exchange').label('source_table')
    ).filter(Exchange.user_id == current_user.id).all()

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
            'currency': record.currency,
            'date': record.date,
            'status': record.status,
            'type': record.source_table,
        }
        for record in combined_transactions
    ]
    return formatted_transactions

# # Example usage
# formatted_transactions = format_combined_transactions()
# for transaction in formatted_transactions:
#     print(transaction)

def generate_card_number(prefix_list, length):
    import random
    """
        Generates a valid card number using the Luhn algorithm.
        :param prefix_list: List of possible starting digits
        :param length: Total length of the card number
        :return: A valid card number as a string
        """
    prefix = random.choice(prefix_list)  # Pick a random prefix from the list
    card_number = [int(x) for x in str(prefix)]

    while len(card_number) < (length - 1):  # Generate remaining digits except the last one
        digit = random.randint(0, 9)
        card_number.append(digit)

    # Luhn algorithm to calculate the last digit
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(''.join(map(str, card_number)))
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        
        return checksum % 10

    checksum = luhn_checksum(card_number)
    card_number.append((10 - checksum) % 10)  # Append the last digit

    return ''.join(map(str, card_number))

def create_card_details(type_):
    import random
    """
    Generates card details based on the type.
    :param type_: The type of card (VISA, MASTERCARD, VERVE, etc.)
    :return: Dictionary containing card details
    """
    if type_ == 'VISA':
        card_number = generate_card_number(["4"], 16)
    elif type_ == 'MASTERCARD':
        card_number = generate_card_number(["51", "52", "53", "54", "55"], 16)
    elif type_ == 'VERVE':
        card_number = generate_card_number(["5061", "5062", "5063", "5078"], 19)
    else:
        raise ValueError("Unsupported card type")

    # Generate expiry date: one year from now
    current_year = datetime.now().year
    expiry_year = (current_year + 1) % 100  # Get last two digits of the year
    expiry_month = f"{datetime.now().month:02d}"  # Keep the current month
    expiry_date = f"{expiry_month}/{expiry_year}"

    details = {
        'user_id': current_user.id,  # Ensure `current_user` is defined
        'card_type': type_,
        'card_holder': current_user.full_name,
        'card_number': card_number,
        'card_expiry': expiry_date,  # Now dynamically generated
        'card_cvv': str(random.randint(100, 999)),  # Generate a random 3-digit CVV
        'card_balance': 0.00,
        'card_status': 'active',
    }
    return details

def connected_wallet():
    current_user.wallet_connected = True
    db.session.commit()
    return True

