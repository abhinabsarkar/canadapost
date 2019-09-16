# Importing my libraries
import requests # Library to invoke REST API using requests
import configparser # Library to read config values
import logger # Custom library to log errors/info. Managed by one central switch
import logging # Library to log exceptions
import urllib3 # Suppress InsecureRequestWarning in the response
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get the html response
def invoke_endpoint(url):
    try:             
        logger.log_message('endpoint url: ' + url)
        # Invoke the endpoint        
        response = requests.get(url, verify=False)
        # Log response        
        logger.log_message('invoke_endpoint return code: ' + response.status_code.__str__())
        logger.log_message('invoke_endpoint reponse text: ' + response.text)
        # Return the html
        return response.text
    except:
        # logging.exception(error)
        raise
