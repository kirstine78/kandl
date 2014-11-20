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
    

# for blog post entry
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
def are_xxxxx_substituted(text):
    """ takes in a string. check if links www.xxxxx and img xxxxx.jpg etc.
        has been substituted by the author.
        Return boolean."""

    if "xxxxx" in text:
        return False
    else:
        return True

    
# for blog - add photos
def are_format_and_img_file_filled_correct(a_format_l_or_p, an_img_file):
    """takes in strings.
        Return boolean. False if any string are empty"""

    if a_format_l_or_p and an_img_file:

        
        the_format = a_format_l_or_p
        the_img_file = an_img_file


        if len(the_format) < 1 or len(the_img_file) < 1:
            return False
        else:
            if the_format == "l" or the_format == "p":
                return True
            else:
                return False
        
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
    



# for blog
def get_older_link(list_of_some_posts, a_number):
    """ Takes in a list_of_some_posts. Based on length of list return a certain string"""

    if len(list_of_some_posts) > a_number:
        return "Older posts &#9658;"
    else:
        return ""
        
    

# for blog
def get_newer_link(list_of_some_posts, a_number):
    """ Takes in a list_of_some_posts. Based on length of list return a certain string"""

    if len(list_of_some_posts) > a_number:
        return "&#9668; Newer posts"
    else:
        return ""


# for photos & videos 
def get_next_link(list_of_some, a_number):
    """ Takes in a list_of_some. Based on length of list return a certain string"""

    if len(list_of_some) > a_number:
        return "Next &#9658;"
    else:
        return ""
        
    

# for photos & videos
def get_previous_link(list_of_some, a_number):
    """ Takes in a list_of_some. Based on length of list return a certain string"""

    if len(list_of_some) > a_number:
        return "&#9668; Previous"
    else:
        return ""

    

# for blog
def is_there_a_tag(some_string):
    """ Takes in a string, return True if string not empty else False """

    if some_string:
        if len(some_string) > 0:
            return True
        else:
            return False
    return False


# for blog used inside blog_post_entry.html. made possible with
# jinja_env.globals.update(selected_value_dropdown=validation.selected_value_dropdown) inside main.py
def selected_value_dropdown(author_chosen, author_option_value):
    """ Takes in two strings: author_chosen, author_option_value
        return a certain string"""
    
    #logging.debug("author_chosen = " + author_chosen)
    #logging.debug("author_option_value = " + author_option_value)

    if author_chosen == author_option_value:
        return "selected"
    else:
        return ""


# for contact
def are_all_contact_fields_filled(name, email, message):
    """ takes in 3 strings.
        Return boolean and 3 strings"""
    
    the_boolean = False

    name_err="Enter your Name"
    email_err="E-mail is incorrect"
    message_err="Write a Message"
    
    if name:
        name_err=""
    if email:

        # check for minimum 3 chars
        if len(email) > 2 and "@" in email and email[-1] != "@" and email[0] != "@" and " " not in email:
            email_err=""
    if message:
        message_err=""
        
        
    if name and email and len(email) > 2 and "@" in email and email[-1] != "@" and email[0] != "@" and " " not in email and message:
        the_boolean=True

    return the_boolean, name_err, email_err, message_err




