from app.database.models import TetherAccount, BitcoinAccount, EthereumAccount  # Import your database models
from app import db


def increase_account_balance_by_interest_rate(model_class):
    accounts = model_class.query.all()

    for account in accounts:
        # Calculate the interest amount
        interest_amount = account.locked_balance * (account.interest_rate / 100)

        # Update the available balance with the interest amount
        # account.available_balance += interest_amount
        account.pending_balance += interest_amount

        # Commit the changes to the database
        try:
            db.session.commit()
            #db.session.close()
        except Exception as e:
            db.session.rollback()
            print(f'==========={e}===========')


# Example usage:
# increase_account_balance_by_interest_rate(TetherAccount, 2.5)  # Increase Tether account balances by 2.5% interest
# increase_account_balance_by_interest_rate(BitcoinAccount, 1.8)  # Increase Bitcoin account balances by 1.8% interest
# increase_account_balance_by_interest_rate(EthereumAccount, 3.0)  # Increase Ethereum account balances by 3.0% interest