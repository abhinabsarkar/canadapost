# Importing my libraries
import requests
# Import json module
import json
# Library to convert string to dictionary
import ast
# Import CSV read & write module
import csv
# Importing configuration parser
import configparser
import logger # Custom library to log errors/info. Managed by one central switch
import logging # Library to log exceptions
# Suppress InsecureRequestWarning in the response
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Parser to read configuration values
config = configparser.ConfigParser()
config.read("config.ini")

# Get client with url, resource & id for an unsecured api
def get(url, resource, id):
    try:
        request_url = url + id + resource
        # Invoke the REST API call
        response = requests.get(request_url, verify=False)
        # returns the status code json encoded content of response, if any
        response_list = [response.status_code, response.text]
        # Log response        
        logger.log_message('get return code: ' + str(response.status_code))
        logger.log_message('get response text: ' + response.text)
        return response_list
    except:
        # logging.exception(error)
        raise