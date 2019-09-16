# Screen scrape from html and extract data

# Importing my libraries
from bs4 import BeautifulSoup # Library to scrape information from web pages
import logger # Custom library to log errors/info. Managed by one central switch
import logging # Library to log exceptions
import inspect # Library to get the current function name

def load_html(html):
    try:
        # Load the html
        soup = BeautifulSoup(html, 'html.parser')
        # Log the result
        logger.log_message(inspect.currentframe().f_code.co_name + ' Loaded html: ' + soup.prettify())
        # return the result
        return soup
    except:
        # logging.exception(error)
        raise

def extract_table(soup, table_class):
    dataset = []
    crs_range = ''
    candidate_count = ''
    try:
        # Extract the table
        table = soup.find("table", attrs={"class":table_class})
        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]
        dataset.append(headings)
        # Iterate through the rows of the table
        for row in table.find_all("tr")[1:]: # Skip the first row
            for th in row.find_all("th"):
                crs_range = th.get_text()        
            for td in row.find_all("td"):
                candidate_count = td.get_text()        
            data = [crs_range, candidate_count]   
            dataset.append(data)
        # Log result count        
        logger.log_message(inspect.currentframe().f_code.co_name + ' returns datasets with count ' + str(len(dataset)))   
        # Return result
        return dataset             
    except:
        # logging.exception(error)
        raise

# Get nth div from beautiful soup object
def extract_div(soup, div_class, div_count):
    try:
        # Extract the table
        div = soup.find_all("div", attrs={"class":div_class})[div_count]
        # Log result        
        logger.log_message(inspect.currentframe().f_code.co_name + ' returns result from div ' + div.prettify())
        # return result
        return div   
    except:
        # logging.exception(error)
        raise

# Pull text from all instances of <p> tag within BodyText div
def extract_text_from_div(div):
    try:
        # Extract the table
        result_list = div.find_all('p')
        # Log result        
        logger.log_message(inspect.currentframe().f_code.co_name + ' returns result text list count ' + str(len(result_list)))
        output_list = []
        # Add heading
        row = [result_list[0].contents, '']
        output_list.append(row)
        # Get the formatted output in a list
        for item in result_list[1:]: # skip the first row
            if 'strong' in str(item.contents):
                # # Extract text from string
                # temp = str(item.contents[0]).replace('/', '')                
                # field = temp.split('<strong>')[1]
                # # Log field text
                # logger.log_message(inspect.currentframe().f_code.co_name + 'field text: ' + field)
                # Add row to the list
                if len(item.contents) > 1:                    
                    row = [item.contents[0], item.contents[1]]
                    output_list.append(row)
                else:
                    row = [item.contents[0], '']
                    output_list.append(row)        
        # Log result        
        logger.log_message(inspect.currentframe().f_code.co_name + ' returns output list count ' + str(len(output_list)))
        # return result
        return output_list   
    except:
        # logging.exception(error)
        raise        

# Get the last modified date
def get_date_modified(soup):
    try:
        # Get the last modified date
        modified_date = soup.find('time').contents
        # Log result
        logger.log_message(inspect.currentframe().f_code.co_name + ' returns modified date: ' + str(modified_date))
        # return result
        return modified_date
    except:
        # logging.exception(error)
        raise