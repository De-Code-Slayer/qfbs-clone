from flask_login import current_user
from app import db
import logging

def update_payment_method(form_data):
    trc_tether_wallet_address = form_data.get('trc_tether_wallet_address')
    erc_tether_wallet_address = form_data.get('erc_tether_wallet_address')
    ethereum_wallet_address = form_data.get('ethereum_wallet_address')
    bitcoin_wallet_address= form_data.get('bitcoin_wallet_address')

    try:
        current_user.trc_tether_wallet_address = trc_tether_wallet_address
        current_user.erc_tether_wallet_address = erc_tether_wallet_address
        current_user.ethereum_wallet_address = ethereum_wallet_address
        current_user.bitcoin_wallet_address = bitcoin_wallet_address

        db.session.commit()


    except Exception as e:
        db.session.rollback()
        logging.error({"error":e})