# -*- coding: cp1252 -*-
from datetime import datetime
from datetime import date
#import info_entered
import logging


### for blog
##def is_date_valid(a_date):
##    """ Takes in a string a_date in "dd-mm-yyyy" format'.
##        Check if there is a date entered AND if it is valid date.
##        Returns boolean"""
##    
##    
##    try:
##        #logging.debug("string passed in: " + a_date)
##        date_object = datetime.strptime(a_date, '%d-%m-%Y').date()  ###################
##        #logging.debug("string passed in AFTER: " + a_date)
##        return True
##            
##    except ValueError:
##        return False
    

# for blog
def are_all_fields_filled(headline, text):
    """takes in strings.
        Return boolean. False if any string are empty"""

    if headline and text:

        
        a_headline = headline
        a_text = text


        if len(a_headline) < 1 or len(a_text) < 1:
            return False
        else:
            return True
        
    else:
        return False




# for blog
def convert_to_letter_month(a_date):
    """ DateTimeProperty with format yyyy-mm-dd 06:46:22.467000 converted to string    dd. April yyyy    and returned """
    
    some_date_str = str(a_date)
    
    dd = some_date_str[8:10]
    yyyy = some_date_str[:4]

    mm = some_date_str[5:7]

    if mm == "01":
        mm = "January"
    elif mm == "02":
        mm = "February"
    elif mm == "03":
        mm = "March"
    elif mm == "04":
        mm = "April"
    elif mm == "05":
        mm = "May"
    elif mm == "06":
        mm = "June"   
    elif mm == "07":
        mm = "July"
    elif mm == "08":
        mm = "August"
    elif mm == "09":
        mm = "September"
    elif mm == "10":
        mm = "October"
    elif mm == "11":
        mm = "November"
    elif mm == "12":
        mm = "December"


    return dd + ". " + mm + " " + yyyy


# for blog
def get_just_yyyy(a_date):
    """ DateTimeProperty with format yyyy-mm-dd 06:46:22.467000 is passed in.
        Return the year as string in format yyyy """

    some_date_str = str(a_date)
    yyyy = some_date_str[:4]

    return yyyy

# for blog
def get_just_mm(a_date):
    """ DateTimeProperty with format yyyy-mm-dd 06:46:22.467000 is passed in.
        Return the year as string in format mm """

    some_date_str = str(a_date)
    mm = some_date_str[5:7]

    return mm


# for blog
def upper_case_first_letter(a_string):
    """ Return string with first letter in upper case """
    if a_string and len(a_string) > 0:
        first_letter_to_upper = a_string[0:1].upper()
        if len(a_string) > 1:
            string_to_upper = first_letter_to_upper + a_string[1:]
        else:
            string_to_upper = first_letter_to_upper
        return string_to_upper
    else:
        return a_string



# for blog
def numeric_to_alpabetic(a_month_number):
    """ Takes in a number for example 10, not a string.
        Return string which is the month written with letters equivalent to number """
    mm = str(a_month_number)
    
    if mm == "1":
        mm = "January"
    elif mm == "2":
        mm = "February"
    elif mm == "3":
        mm = "March"
    elif mm == "4":
        mm = "April"
    elif mm == "5":
        mm = "May"
    elif mm == "6":
        mm = "June"   
    elif mm == "7":
        mm = "July"
    elif mm == "8":
        mm = "August"
    elif mm == "9":
        mm = "September"
    elif mm == "10":
        mm = "October"
    elif mm == "11":
        mm = "November"
    elif mm == "12":
        mm = "December"


    return mm
    



        
    


##################################################################################################################

def is_food_item_valid(food_description):
    """ Checks if food_description is not None and if length is > 0.
        Creates an object of classInfoEntered and returns it """

    if food_description and len(food_description) > 0:
        obj_food = info_entered.InfoEntered(True, "")  # create object of class InfoEntered
        return obj_food
    else:
        obj_food = info_entered.InfoEntered(False, "You need a 'Food Item'") # create object of class InfoEntered
        return obj_food
        

     
def are_all_validation_true(list_of_info_entered_objects):
    """ Takes in a list of objects and return True if all objects instance variable 'validation' are True """

    for item in list_of_info_entered_objects:
        if item.get_validation_info() == False:
            return False
    return True



def is_future_date(a_date):
    """ Takes in a DateObject yyyy-mm-dd and returns True if it is younger than current date yyyy-mm-dd """
    
    today = date.today() #yyyy-mm-dd
    
    return today <= a_date


def expires_soon(date_to_check):
    """ return boolean, int
        True if date_to_check yyyy-mm-dd is within x days to expire, and amount of days before exp """

    LIMIT_FOR_EXPIRES_SOON = 7

    
    today = date.today() #yyyy-mm-dd

    # difference between current date and date_to_check in format 'x days, 0:00:00'
    diff = date_to_check - today

    #convert to string
    diff_str =  str(diff)
    
    first_ch = diff_str[0:1]

    # split 'x days, 0:00:00' and put into list
    word_list = diff_str.split( )
    first_word = str(word_list[0]) # this is the number of days difference as string

    # expired
    if first_ch == "-": 
        return True, int(first_word)
    # expires today
    elif first_ch == "0":
        return True, 0
    # check if expires soon
    else:
        get_int = int(word_list[0])
        # expires soon
        if get_int <= LIMIT_FOR_EXPIRES_SOON:
            return True, int(first_word)
        # not to expire soon
        return False, int(first_word)

def days_in_freezer(date_when_added):
    """ date_when_added in format yyyy-mm-dd. Returns (an int) how many days since item
        was added in freezer compared with current date. """

    today = date.today() #yyyy-mm-dd

    # difference between current date and date_when_added in format 'x days, 0:00:00'
    diff = today - date_when_added
    
    diff_str =  str(diff)  # convert to string

    first_ch = diff_str[0:1]

    if first_ch == "0":  # 0 days since added to freezer
        return int(first_ch)
    else:  # more than 0 days since added to freezer
        word_list = diff_str.split( )
        first_word = str(word_list[0])
        get_int = int(word_list[0])
        return get_int
    


def get_number_code(sort_string):
    """ takes in a string sort_string (e.g. "created DESC") and return a corresponding int"""

    if sort_string == "created DESC":  # use created cause it's more precise than 'added_date'
        number = 1
        
    elif sort_string=="lower_case_description ASC":
        number = 2
        
    elif sort_string=="lower_case_description DESC":
        number = 3

    elif sort_string=="created ASC":
        number = 4
        
    elif sort_string=="created DESC":
        number = 5
        
    elif sort_string=="expiry ASC":
        number = 6
        
    else: # sort_string=="expiry DESC":
        number = 7

    return number

    
    
def get_param(an_int_in_a_string):
    """ takes in a string an_int_in_a_string (which is a number as strin,g ex. "2"), convert it to an int
        and return a corresponding string"""

    an_int = int(an_int_in_a_string)

    if an_int == 1:
        param = "created DESC"

    elif an_int == 2:
        param = "lower_case_description ASC"
        
    elif an_int == 3:
        param = "lower_case_description DESC"

    elif an_int == 4:
        param = "created ASC"

    elif an_int == 5:
        param = "created DESC"

    elif an_int == 6:
        param = "expiry ASC"

    else:  # an_int == 7:
        param = "expiry DESC"

    return param

def convert_DateProperty_to_str_slash(date):
    """ convert a DateProperty a_date with format yyyy-mm-dd to a string with format "mm/dd/yyyy" """

    date_string = str(date)
    
    mm = date_string[5:7]
    dd = date_string[-2:]
    yyyy = date_string[0:4]

    # return dd + "-" + mm + "-" + yyyy
    return mm + "/" + dd + "/" + yyyy

def convert_DateProperty_to_str_dash(date):
    """ convert a DateProperty a_date with format yyyy-mm-dd to a string with format "dd-mm-yyyy" """

    date_string = str(date)
    
    mm = date_string[5:7]
    dd = date_string[-2:]
    yyyy = date_string[0:4]

    return dd + "-" + mm + "-" + yyyy



### for blog
##def convert_to_letter_month(a_date):
##    """ DateProperty with format yyyy-mm-dd converted to string    dd. April yyyy    and returned """
##    
##    some_date_str = str(a_date)
##    
##    dd = some_date_str[-2:]
##    yyyy = some_date_str[:4]
##
##    mm = some_date_str[5:7]
##
##    if mm == "01":
##        mm = "January"
##    elif mm == "02":
##        mm = "February"
##    elif mm == "03":
##        mm = "March"
##    elif mm == "04":
##        mm = "April"
##    elif mm == "05":
##        mm = "May"
##    elif mm == "06":
##        mm = "June"   
##    elif mm == "07":
##        mm = "July"
##    elif mm == "08":
##        mm = "August"
##    elif mm == "09":
##        mm = "September"
##    elif mm == "10":
##        mm = "October"
##    elif mm == "11":
##        mm = "November"
##    elif mm == "12":
##        mm = "December"
##
##
##    return dd + ". " + mm + " " + yyyy
