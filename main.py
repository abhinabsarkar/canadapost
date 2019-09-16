# Importing my libraries
import configparser
import json
import os 
import time
import logging
import logger
import sys, traceback
import get_html
import screen_scraper
import notify
import response_format
import HTML
from datetime import datetime
import file_mgmt
import api_client

# Parser to read configuration values
config = configparser.ConfigParser()
config.read("config.ini")

try:
    # Log the start of the process    
    logger.log_note('*** Job initiated at ' + str(datetime.today()) + ' ***')
    # Check for the log files and purge, if they are other than today's date
    timestamp = time.strftime("%Y%m%d")    
    logfilename = timestamp + ".log"
    log_list = file_mgmt.list_files(os.getcwd(), 'log')
    for log in log_list:
        if log != logfilename:
            file_mgmt.delete_file(log)
    # Invoke the endpoint
    logger.log_note('Invoke the CanadaPost API endpoint')
    response_list = api_client.get(config['Default']['canadapost_tracking'], \
        config['Default']['canadapost_resource'], config['Default']['tracking_number'])
    if int(response_list[0]) == 200:           
        # Load the json document into a python object        
        json_response = json.loads(response_list[1])
        logger.log_note('Loaded the json document into python object')
        # Check if the property 'events' exist                    
        if "events" in json_response:            
            # Get the current event count
            event_count = len(json_response['events'])
            logger.log_note(str(event_count) + ' events recorded')
            # If the event_count is greater than last_event_count, notify
            if event_count > int(config['Default']['last_event_count']):
                logger.log_note('New event(s) recorded')
                # Get the first item from the 'events' array in the json response for sms
                sms_msg = str(json_response["events"][0]["descEn"]) + ' at ' + \
                    str(json_response["events"][0]["locationAddr"]["city"]) + ',' + \
                    str(json_response["events"][0]["locationAddr"]["countryNmEn"]) 
                logger.log_note('SMS message for the latest event created')                   
                # Create a list of events for email message body
                row = ['Date', 'Time', 'Progress']
                package_progress_list = []
                package_progress_list.append(row)
                for item in json_response["events"]:                    
                    date = item["datetime"]["date"]
                    time = item["datetime"]["time"]
                    # If location is there in the event, append to the update else leave it
                    if "locationAddr" in item:
                        progress = item["descEn"] + ' at ' + item["locationAddr"]["city"] + ',' + \
                            item["locationAddr"]["countryNmEn"]
                    else:
                        progress = item["descEn"]
                    row = [date, time, progress] 
                    package_progress_list.append(row)                
                logger.log_note('List of events for the email message body created')
                # Format the email body to html format 
                body = response_format.html_result(package_progress_list)              
                logger.log_note('Email body formatted to html')                 
                # Send notification for every new event 
                notify.send_sms('Canada Post status update pkg # ' + config['Default']['tracking_number'] + ' - ' + sms_msg, \
                    config['Default']['account_sid'], config['Default']['auth_token'])
                logger.log_note('SMS for the new event sent')
                notify.send_email('Canada Post status update pkg # ' + config['Default']['tracking_number'], body, \
                    config['Default']['sendgrid_key'])
                logger.log_note('Email for the list of events along with the new event sent')
                # Update the last_event_count
                config.set('Default', 'last_event_count', str(event_count))               
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)        
                logger.log_note('New event count is updated in config file as ' + str(event_count))
                # Log message that the job has completed
                logger.log_note('*** Job completed at ' + str(datetime.today()) + ' ****')
            else:
                logger.log_note('No new event found')
                # Log message that the job has completed
                logger.log_note('*** Job completed at ' + str(datetime.today()) + ' ****')
        else:
            if "error" in json_response:                              
                if "descEn" in json_response["error"]:                     
                    logger.log_note(json_response["error"]["descEn"])
            logger.log_note('*** Job completed at ' + str(datetime.today()) + ' ****')
except Exception as error:
    # Log the error message & send notification
    logger.log_error(error)
    body = 'Error occured: ' + str(error) + '. Check logs for more details.'
    # Set the counter for the first error notification of the day
    if str(datetime.today().date()) != config['Default']['max_notification_date']:
        counter = 0
        # reset the counter
        config.set('Default', 'error_notification_count', str(counter))               
        with open('config.ini', 'w') as configfile:
            config.write(configfile)        
    # Get error notification count
    counter = int(config['Default']['error_notification_count']) + 1
    if counter <= int(config['Default']['max_notification_count']):
        notify.send_sms('Canada Post notification ' + str(counter) + ' ' + body, config['Default']['account_sid'], \
            config['Default']['auth_token'])
        notify.send_email('Canada Post error ' + str(counter) + '- Please see the error below', body, \
            config['Default']['sendgrid_key']) 
        # Log the error notification count of the day
        if counter == int(config['Default']['max_notification_count']):
            # Log the max error notification as the last notification
            logger.log_note('This is the last error notification for the date - ' + str(datetime.today()))        
        else:
            logger.log_note('Error notification ' + str(counter) + ' sent on ' + str(datetime.today()))

        # Updating the configuration file with error_notification_count & max_notification_date
        config.set('Default', 'error_notification_count', str(counter)) 
        config.set('Default', 'max_notification_date', str(datetime.today().date()) )               
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        logger.log_note('No notification sent for this error log since the max notification counter is crossed')
    # Log message that the job has failed
    logger.log_note('*** Job failed at ' + str(datetime.today()) + ' ****')