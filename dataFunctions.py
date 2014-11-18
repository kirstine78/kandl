import random
import string
import math

from google.appengine.ext import db
import main



def retrieveUser(userName):
    """ Takes a string userName and return the user (item in ru db)
        with that name from the db"""
    
    all_reg_users = db.GqlQuery("SELECT * FROM RegisteredUsers ORDER BY created DESC")

    if all_reg_users:
        for user in all_reg_users:
            if user.name == userName:
                return user
    return None


def retrieveUserId(userName):
    """ Takes in a string userName and return the int id of a user """
    current_user = retrieveUser(userName)  # ru object
    if current_user:
        return current_user.key().id()
    return None


#### for blog posts ###

def find_all_blog_posts():
    """ Perform db.GqlQuery and returns all blog posts from database """
    return find_limited_blog_posts(1000)


def find_limited_blog_posts(max_results):
    """ Takes a number max_results and perform db.GqlQuery and returns blog posts from database within limit of max_results """

    limited_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(max_results)
    return limited_blog_posts



def find_newer_blog_posts(max_results, date_time):
    """ Takes a number max_results and a date_time, then perform db.GqlQuery and
        returns blog posts from database where 'created' is bigger than date_time (newer posts)"""
    
    newer_blog_posts = db.GqlQuery("SELECT * FROM BlogPost WHERE created > :1 ORDER BY created ASC", date_time).fetch(max_results)

    return newer_blog_posts


def find_older_blog_posts(max_results, date_time):
    """ Takes a number max_results and a date_time, then perform db.GqlQuery and
        returns blog posts from database where 'created' is smaller than date_time (older posts)"""
    
    older_blog_posts = db.GqlQuery("SELECT * FROM BlogPost WHERE created < :1 ORDER BY created DESC", date_time).fetch(max_results)

    return older_blog_posts


def find_blog_posts_between(max_results, date_time_oldest, date_time_youngest):
    """ Takes a number max_results and two dateTimes: date_time_youngest and date_time_oldest.
        Then perform db.GqlQuery and returns blog posts from database where 'created' is in between the two dateTimes """
    
    in_between_blog_posts = db.GqlQuery("SELECT * FROM BlogPost where created > :1 AND created < :2 ORDER BY created DESC", date_time_oldest, date_time_youngest).fetch(max_results)

    return in_between_blog_posts


def find_blog_posts_between_and_younger(max_results, date_time_oldest, date_time_youngest, id_blog_post):
    """ Takes a number max_results and two dateTimes: date_time_youngest and date_time_oldest, and an id_blog_post.
        Then perform db.GqlQuery and returns blog posts from database where 'created' is in between the two dateTimes and where
        posts are younger than post with id_blog_post"""

    specific_blog_post = main.BlogPost.get_by_id(int(id_blog_post))
    
    in_between_and_younger_blog_posts = db.GqlQuery("SELECT * FROM BlogPost where created > :1 AND created < :2 AND created > :3 ORDER BY created ASC", date_time_oldest,
                                                    date_time_youngest, specific_blog_post.created).fetch(max_results)

    return in_between_and_younger_blog_posts

def find_blog_posts_between_and_older(max_results, date_time_oldest, date_time_youngest, id_blog_post):
    """ Takes a number max_results and two dateTimes: date_time_youngest and date_time_oldest, and an id_blog_post.
        Then perform db.GqlQuery and returns blog posts from database where 'created' is in between the two dateTimes and where
        posts are older than post with id_blog_post"""

    specific_blog_post = main.BlogPost.get_by_id(int(id_blog_post))
    
    in_between_and_older_blog_posts = db.GqlQuery("SELECT * FROM BlogPost where created > :1 AND created < :2 AND created < :3 ORDER BY created DESC", date_time_oldest,
                                                    date_time_youngest, specific_blog_post.created).fetch(max_results)

    return in_between_and_older_blog_posts


### for photos ###

def find_all_photos():
    """ Perform db.GqlQuery and returns all photos from database """
    return find_limited_photos(1000)


def find_limited_photos(max_results):
    """ Takes a number max_results and perform db.GqlQuery and returns photos from database within limit of max_results """

    limited_photos = db.GqlQuery("SELECT * FROM Photo ORDER BY created DESC").fetch(max_results)
    return limited_photos

def find_newer_photos(max_results, date_time):
    """ Takes a number max_results and a date_time, then perform db.GqlQuery and
        returns photos from database where 'created' is bigger than date_time (newer photos)"""
    
    newer_photos = db.GqlQuery("SELECT * FROM Photo WHERE created > :1 ORDER BY created ASC", date_time).fetch(max_results)

    return newer_photos


def find_older_photos(max_results, date_time):
    """ Takes a number max_results and a date_time, then perform db.GqlQuery and
        returns photos from database where 'created' is smaller than date_time (older photos)"""
    
    older_photos = db.GqlQuery("SELECT * FROM Photo WHERE created < :1 ORDER BY created DESC", date_time).fetch(max_results)

    return older_photos


# Photo helper function to organize the rows correctly
def get_rows_of_photos_list_of_list(list_of_photos_db_query, max_img_each_row_decimal, max_img_each_row_integer):
    """ Takes a list of photos (list_of_photos_db_query), two numbers (max_img_each_row_decimal & max_img_each_row_integer)
        returns a list of lists with each inner list representing a row with img's """

    all_the_photos = list_of_photos_db_query
    length_all_photos = len(all_the_photos)
    
    MAX_IMGS_ON_ROW_DECIMAL = max_img_each_row_decimal
    MAX_IMGS_ON_ROW_INT = max_img_each_row_integer

    
    # how many rows do we need: len(all_the_photos) / MAX_IMGS_ON_ROW_DECIMAL
    rows_needed_decimal = length_all_photos / MAX_IMGS_ON_ROW_DECIMAL
##            logging.debug("rows_needed_decimal = " + str(rows_needed_decimal))

    # always round up
    rows_needed_round = math.ceil(rows_needed_decimal)
##            logging.debug("rows_needed_round = " + str(rows_needed_round))

    # convert to an integer
    rows_needed_int = int(rows_needed_round)
##            logging.debug("rows_needed_int = " + str(rows_needed_int))

    if (length_all_photos % MAX_IMGS_ON_ROW_INT) != 0:   # fully filled rows will be one less than total rows
##                logging.debug("goes into not equal zero")
        rows_fully_filled = rows_needed_int - 1
        
    else:  # no leftovers (that means no row that is not fully filled)
##                logging.debug("goes into equal zero")
        rows_fully_filled = rows_needed_int

    # calculate how many img's there shall be in the the row not fully filled    
    amount_img_in_row_not_filled = length_all_photos % MAX_IMGS_ON_ROW_INT
##            logging.debug("rows_fully_filled = " + str(rows_fully_filled))
##            logging.debug("amount_img_in_row_not_filled = " + str(amount_img_in_row_not_filled))

    # create a list of lists where each inner list represents a row (We have decided max 7 img's in a row)
    list_of_lists = []  # will become a list of lists with each inner list representing a row with img's
    
    counter = 0
    for photo in range(rows_fully_filled):
        single_row = []
        for i in range (MAX_IMGS_ON_ROW_INT):
            single_row.append(all_the_photos[counter])
            counter = counter + 1
        list_of_lists.append(single_row)
##            logging.debug("length outer list = " + str(len(list_of_lists)))

    # only if we need a not fully filled row do the following if statement
    if (length_all_photos % MAX_IMGS_ON_ROW_INT) != 0:
##                logging.debug("we construct a not full row")
        single_row = []  
        for img in range(amount_img_in_row_not_filled):
            single_row.append(all_the_photos[counter])
            counter = counter + 1
        list_of_lists.append(single_row)
        
    
##            logging.debug("length outer list = " + str(len(list_of_lists)))

    return list_of_lists

                
    

###########################################################################################################
def randomword():
    """return a random string"""
    length = randomLength()
    alpha = "abcdefghijklmnopqrstuvwABCDEFGHIJKLMNOPQRSTUVW"
    return ''.join(random.choice(alpha) for i in range(length))
    


def randomLength():
    """ return random int between 4 and 6"""
    return random.randint(4, 6)
