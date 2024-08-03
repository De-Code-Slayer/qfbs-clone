import requests
import os
import logging

COIN_LAYER_API_KEY = os.getenv('COIN_LAYER_API_KEY')

def get_usd_to_() -> dict:
    try:
        exchang_rate = requests.get(f'http://api.coinlayer.com/api/live?access_key={COIN_LAYER_API_KEY}&symbols=BTC,ETH,USDT&target=USD')
    except Exception as e:
        logging.error(f'could not get currency exchange rate: {str(e)}')
        return {'BTC': 29639.892987, 'ETH': 1883.490822, 'USDT': 1}
    return {'BTC': 29639.892987, 'ETH': 1883.490822, 'USDT': 1} #exchang_rate.json().get('rates')
    
