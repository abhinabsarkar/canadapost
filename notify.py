# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logger # Custom library to log errors/info. Managed by one central switch
import logging # Library to log exceptions
import inspect # Library to get the current function name
from twilio.rest import Client # Library to send messages using twilio

def send_email(subject, body, sendgrid_key):
    message = Mail(
        from_email='crs@absplay.com',
        to_emails='abhinab.sarkar@hotmail.com',
        subject=subject,
        html_content=body)
    try:
        sg = SendGridAPIClient(sendgrid_key)
        response = sg.send(message)
        # Log the result
        logger.log_note(inspect.currentframe().f_code.co_name + ' response.code ' + str(response.status_code))        
    except:
        # logging.exception(error)
        raise

def send_sms(message, taccount_sid, tauth_token):
    try:
        # Your Account Sid and Auth Token from twilio.com/console
        account_sid = taccount_sid
        auth_token = tauth_token
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=message,
                            from_='+12264076158',
                            to='+14372294588'
                        )
        # Log the result
        logger.log_message(inspect.currentframe().f_code.co_name + ' sms sent ' + str(message.sid))
    except:
        # logging.exception(error)
        raise