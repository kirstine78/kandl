import random
import string

from google.appengine.ext import db



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



###########################################################################################################
def randomword():
    """return a random string"""
    length = randomLength()
    alpha = "abcdefghijklmnopqrstuvwABCDEFGHIJKLMNOPQRSTUVW"
    return ''.join(random.choice(alpha) for i in range(length))
    


def randomLength():
    """ return random int between 4 and 6"""
    return random.randint(4, 6)
