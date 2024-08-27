from app import db
from flask_login import UserMixin
from datetime import datetime



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.String(255), nullable=True)
    sex = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    temporary_address = db.Column(db.String(255),nullable=True, default='')
    permanent_address = db.Column(db.String(255), nullable=True, default='')
    phone_code= db.Column(db.String(255), nullable=False, default='')
    phone= db.Column(db.String(255), nullable=False, default='')


    transactions = db.relationship('Transactions', backref='trx_user', lazy=True)
    
    gas_fee = db.Column(db.Float, nullable=False, default=0.05)

    # acoins
    
    btc = db.relationship('BTC', uselist=False, backref='btc_cn', lazy=True)
    sol = db.relationship('SOL', uselist=False, backref='sol_cn', lazy=True)
    eth = db.relationship('ETH', uselist=False, backref='eth_cn', lazy=True)
    ripple = db.relationship('RIPPLE', uselist=False, backref='ripple_cn', lazy=True)
    usdt = db.relationship('USDT', uselist=False, backref='usdt_cn', lazy=True)
    stellar = db.relationship('STELLAR', uselist=False, backref='stellar_cn', lazy=True)
    xdc = db.relationship('XDC', uselist=False, backref='xdc_cn', lazy=True)
    algo = db.relationship('ALGO', uselist=False, backref='algo_cn', lazy=True)
    poly = db.relationship('POLY', uselist=False, backref='poly_cn', lazy=True)
    fix_d = db.relationship('Fixed_DepositTRX', uselist=False, backref='fix_d_tr', lazy=True)
    dep_trx = db.relationship('DepositTRX', uselist=False, backref='d_tr', lazy=True)
    


    # withdrawal address
    trc_tether_wallet_address = db.Column(db.String(255), nullable=True, default='')
    erc_tether_wallet_address = db.Column(db.String(255), nullable=True, default='')
    ethereum_wallet_address = db.Column(db.String(255), nullable=True, default='')
    bitcoin_wallet_address = db.Column(db.String(255), nullable=True, default='')


    # verifications
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    verified  = db.Column(db.Boolean, nullable=False, default=False) 


    
    display_photo = db.Column(db.String(255), nullable=True, default='https://www.gravatar.com/avatar/3aa90a79fc58869002a4530b5ef342f9?s=500&amp;d=mp')
    postal_code = db.Column(db.String(255), nullable=False)
    
    
    
    referer = db.relationship('Referrals', backref='reff_user', lazy=True, foreign_keys='Referrals.username')
    

class BTC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class SOL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class ETH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class RIPPLE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class USDT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class ALGO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class STELLAR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class XDC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    
class POLY(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    coin = db.Column(db.String(255))
    coin_short = db.Column(db.String(255))
    amount = db.Column(db.Float, default=0.000)
    




class Transactions(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        currency = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255), default='processing')
        # Add more fields as needed



class Referrals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    reffered_user_name = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Add more fields as needed



class Fixed_DepositTRX(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        plan = db.Column(db.String(255))
        tenure = db.Column(db.String(255))
        interest = db.Column(db.Float)
        min_amount = db.Column(db.Float)
        max_amount = db.Column(db.Float)
        amount = db.Column(db.Float)
        date = db.Column(db.DateTime, default=datetime.now)
        # Add more fields as needed

class DepositTRX(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        curency = db.Column(db.String(255))
        amount = db.Column(db.Float)
        wallet = db.Column(db.String(255))
        date = db.Column(db.DateTime, default=datetime.now)
        # Add more fields as needed

class SendMoney(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        recepient_email = db.Column(db.String(255))
        currency = db.Column(db.String(255))
        amount = db.Column(db.Float)
        note = db.Column(db.String(255))
        charge_recepient = db.Column(db.Boolean, default=False)
        date = db.Column(db.DateTime, default=datetime.now)
        type = db.Column(db.String(255), default='outgoing')
        status = db.Column(db.String(255), default='processing')
        action = db.Column(db.String(255))
        # Add more fields as needed

class RequestMoney(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        recepient_email = db.Column(db.String(255))
        currency = db.Column(db.String(255))
        wallet = db.Column(db.String(255))
        amount = db.Column(db.Float)
        note = db.Column(db.String(255))
        date = db.Column(db.DateTime, default=datetime.now)
        type = db.Column(db.String(255), default='outgoing')
        status = db.Column(db.String(255))
        action = db.Column(db.String(255))

class Exchange(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        from_wallet = db.Column(db.String(255))
        to_wallet = db.Column(db.String(255))
        amount = db.Column(db.Float)
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed

class Redeem(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        recepient_email = db.Column(db.String(255))
        currency = db.Column(db.String(255))
        amount = db.Column(db.Float)
        note = db.Column(db.String(255))
        date = db.Column(db.DateTime, default=datetime.now)
        type = db.Column(db.String(255))
        status = db.Column(db.String(255))
        
        # Add more fields as needed

class Escrow(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        recepient_email = db.Column(db.String(255))
        currency = db.Column(db.String(255))
        amount = db.Column(db.Float)
        note = db.Column(db.String(255))
        date = db.Column(db.DateTime, default=datetime.now)
        type = db.Column(db.String(255))
        status = db.Column(db.String(255))

class Dispute(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        coin = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed

class QrPayment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        coin = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed

class QFS(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        coin = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed

class Voucher(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        coin = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed

class Invoice(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        coin = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed

class Bill(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        coin = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed

class Payout(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
        transaction_type = db.Column(db.String(255))
        coin = db.Column(db.String(255))
        amount = db.Column(db.Float)
        trx_type = db.Column(db.String(255))
        timestamp = db.Column(db.DateTime, default=datetime.now)
        status = db.Column(db.String(255))
        # Add more fields as needed
