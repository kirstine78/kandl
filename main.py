#!/usr/bin/env python
# -*- coding: cp1252 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#########################
#                       #
#    The Blog           #
#     kandl             #
#########################

# -*- coding: cp1252 -*-

import validation
import dataFunctions
import passwordValid

import emailFunctions

import math
import cgi
import re
import os
import webapp2
import jinja2
import random
import string
import hashlib
import time
import logging
from datetime import datetime
from datetime import date
from google.appengine.ext import db


# if name of folder where img's are is changed then change the constant name to the same
BLOG_IMAGES_LOCATION = "../images/blog/"  # used in validation.do_substitutions
BLOG_VIDEOS_LOCATION = "../videos/"   # used in validation.do_substitutions

GALLERY_IMAGES_LOCATION = "../images/gallery/"  # uses this in # '/photos'   class AllPhotos(Handler)
GENERAL_IMAGES_LOCATION = "../images/general/"  # for example the top image in the base layout


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=False)
jinja_env.globals.update(format_the_date=validation.convert_to_letter_month)  # lets me use validation inside html.
jinja_env.globals.update(numeric_to_alphabetic_month=validation.numeric_to_alpabetic)  # lets me use validation inside html.
jinja_env.globals.update(selected_value_dropdown=validation.selected_value_dropdown)  # lets me use validation inside html.
jinja_env.globals.update(do_substitutions=validation.do_substitutions)  # lets me use this inside html.
jinja_env.globals.update(length=len)
jinja_env.globals['gallery_images_location']=GALLERY_IMAGES_LOCATION
jinja_env.globals['general_images_location']=GENERAL_IMAGES_LOCATION




    
def add_response_headers(response):
    response.headers.add_header("Cache-Control", "no-cache, no-store, must-revalidate") # HTTP 1.1.
    response.headers.add_header("Pragma", "no-cache")  # HTTP 1.0.
    response.headers.add_header("Expires", "0")    # Proxies.
    

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        add_response_headers(self.response)
        self.write(self.render_str(template, **kw))
        

class BlogPost(db.Model): # abbreviated 'bp'
    headline = db.StringProperty(required = False)
    text = db.TextProperty(required = False)
    author = db.StringProperty(required = False)

    created = db.DateTimeProperty(auto_now_add = True)  # more precise date, when sorting with format yyyy-mm-dd 06:46:22.467000
    _string_date_new = ""


class RegisteredUsers(db.Model):  #  --> ru
    name = db.StringProperty(required = True)
    password_hashed = db.StringProperty(required = True)  # (name + pw + salt) hexdigested and then pipe salt with format "hexdigestedValue|salt"
    created = db.DateTimeProperty(auto_now_add = True)


class Photo(db.Model): # abbreviated 'photo'
    img_format = db.StringProperty(required = False)
    img = db.StringProperty(required = False)
    txt_below_img = db.StringProperty(required = False)

    created = db.DateTimeProperty(auto_now_add = True)  # more precise date, when sorting with format yyyy-mm-dd 06:46:22.467000


class Video(db.Model): # abbreviated 'video'
    iframe_tag_and_content = db.StringProperty(required = True)

    created = db.DateTimeProperty(auto_now_add = True)  # more precise date, when sorting with format yyyy-mm-dd 06:46:22.467000
    


def check_user_id_cookie(a_request):
    """"Returns a specific registered user, or if user_id_cookie_value or username is None
        return None"""
    
    user_id_cookie_value = a_request.cookies.get('user_id')# username_input|hash (cookie)
    
    if user_id_cookie_value:
        username = passwordValid.check_secure_val(user_id_cookie_value)
        
        if username:  # valid cookie:
            the_RU = dataFunctions.retrieveUser(username)
            return the_RU
    return None


def make_dict_blog():
    """ Return a dictionary with format example:
        {'2014':{'12':['p1', 'p2', 'p3'], '11':['p4', 'p5'], '8':['p6', 'p7']}, '2013':{'12':['p8', 'p9'], '8':['p1', 'p2']}}
        """

    # get all blogposts
    all_blog_posts = dataFunctions.find_all_blog_posts()
    
    dictionary = {}  # {'2014':{'12':['p1', 'p2', 'p3'], '11':['p4', 'p5'], '8':['p6', 'p7']}, '2013':{'12':['p8', 'p9'], '8':['p1', 'p2']}}

    for blog_post in all_blog_posts:
        a_year = validation.get_just_yyyy(blog_post.created)  # get string yyyy
        a_month = str(int(validation.get_just_mm(blog_post.created)))  # get string mm and make the format 1,2,3,4,5,6,7,8,9,10,11,12

        if a_year not in dictionary:
            dictionary[a_year] = {} # add a_year as key to the dict with empty dict as value

            
            if a_month not in dictionary[a_year]:  # a_month not a key in inner dict for that year
                
                # make a_month a key with empty list as value
                dictionary[a_year][a_month] = []

                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_post)


            else:
                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_post)

        else:
            if a_month not in dictionary[a_year]:  # a_month not a key in inner dict for that year
                
                # make a_month a key with empty list as value
                dictionary[a_year][a_month] = []

                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_post)


            else:
                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_post)
    return dictionary




    
# '/', LoginHandler
class LoginHandler(Handler):
    def write_form(self, a_username="", an_invalid_error=""):
        self.render("login_adm.html", the_login_username=a_username, error_login=an_invalid_error)

        
    def get(self):
        self.write_form()


    def post(self):
        login_username_input = self.request.get('login_username')
        login_password_input = self.request.get('login_password')
        checkbox_stay_loggedIn = self.request.get('stay_logged_in')

        #check if username exists
        user_already_exists = False
        all_reg_users = db.GqlQuery("SELECT * FROM RegisteredUsers ORDER BY created DESC")

        if all_reg_users:
            for users in all_reg_users:
                if users.name == login_username_input:
                    user_already_exists = True
                    the_user_hash = users.password_hashed
                    break
            if user_already_exists:
                #check if password is correct
                if passwordValid.valid_pw(login_username_input, login_password_input, the_user_hash):
                    secure_username = passwordValid.make_secure_val(login_username_input) # return login_username_input|hash
                    

                    if checkbox_stay_loggedIn:
                        # make sure to set cookie expire to never
                        #logging.debug("checkbox_stay_loggedIn")
                        self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/; expires=Fri, 31-Dec-9999 10:05:41 GMT;' %str(secure_username))
                    else:
                        # cookie expire when???
                        #logging.debug("NOT checkbox_stay_loggedIn")
                        self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' %str(secure_username))

                    self.redirect("/add_blog_post")
                else:
                    self.loginError(login_username_input)
            else:
                if login_username_input:
                    self.loginError(login_username_input)
                else:
                    self.loginError("")
        else:
            self.loginError("")


    def loginError(self, name):
        error_log_in = "Invalid login"
        self.write_form(name, error_log_in)


        
# '/logout', LogoutHandler 
class LogoutHandler(Handler):
    def get(self):            
        #set cookie value to 'empty'
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

        #then redirect to '/'
        self.redirect("/")



########## DON'T DELETE THE BELOW ##########################################################################################################

### '/add_user', SignupHandler
##class AddUserHandler(Handler):
##        
##    
##    def get(self):
##        #secure_value # this is the (name + pw + salt) hexdigested and then pipe salt with format "hexdigestedValue|salt"
##        
##        username_input = ""
##        password_input = ""
##
##        
##                    
##            
##
##        # username_and_password = username_input + password_input
##        secure_password = passwordValid.make_pw_hash(username_input, password_input)  # the function returns hash|salt
##        #secure_username = passwordValid.make_secure_val(username_input) # the function returns username_input|hash
##
##       
##        ru = RegisteredUsers(name = username_input, password_hashed = secure_password) # save the hashed password in database
##        ru.put()
##        #time.sleep(0.1)  # to delay so db table gets displayed correct
##        #self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' %str(secure_username))#sending secure_username back to browser
##        self.redirect("/")

########## DON'T DELETE THE ABOVE ##########################################################################################################


        
# '/add_blog_post'    
class AddNewBlogPost(Handler):
    def render_AddNewBlogPost(self, error_msg, bp_db, an_author):
        
        self.render("blog_post_entry.html", error_message=error_msg, bp=bp_db, author_chosen=an_author)


    def render_blank_blog_post(self):
        # create BlogPost item in db
        bp = BlogPost(headline = "", text = "")
        
        self.render_AddNewBlogPost("", bp, "by Kirstine Brørup Nielsen")

 
    def get(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.render_blank_blog_post()
        else:
            # false user, not logged in
            self.redirect('/logout')


    def post(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.process_post()
        else:
            # false user, not logged in
            self.redirect('/logout')


    def process_post(self):            
        # data that user has entered
        headline_blog_messy = self.request.get("headline").strip()  # a string
        text_blog = self.request.get("text").strip()  # a text area...
        author_blog = self.request.get("author_blog_post") 
        
        #make sure first letter in string is upper case
        headline_blog = validation.upper_case_first_letter(headline_blog_messy)
                
        # create BlogPost item in db
        bp = BlogPost(headline = headline_blog, text = text_blog, author = author_blog)
               
        # check if all mandatory fields are filled out
        if validation.are_all_fields_filled(headline_blog, text_blog):

            # then also check if links www.xxxxx and img xxxxx.jpg has been substituted by the author
            if validation.are_xxxxx_substituted(text_blog):
                bp.put()
                #display blank page
                # render "blog_post_entry.html"!
                self.render_blank_blog_post()
                
            else:  # xxxxx is not substituted
                # render "blog_post_entry.html" and display error message and redisplay what was filled in
                self.render_AddNewBlogPost("Substitute the 'xxxxx'", bp, author_blog)
            
            
        else:  # not all mandatory fields are filled out
            # render "blog_post_entry.html" and display error message and redisplay what was filled in
            self.render_AddNewBlogPost('Headline and/or Text missing', bp, author_blog)

            

# '/edit_blog_post', EditBlogPost
class EditBlogPost(Handler):
    def render_EditBlogPost(self, list_of_posts):
        
        self.render("blog_post_edit.html", blog_posts=list_of_posts)

    def get(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            all_blog_posts = dataFunctions.find_all_blog_posts()
            
            self.render_EditBlogPost(all_blog_posts)
        else:
            # false user, not logged in
            self.redirect('/logout')


    def post(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            # id data (which check boxes has administrator checked) put in a variable
            list_of_id_checked = self.request.get_all("delete")  # returns a list of id strings

            # delete button data (if delete button clicked, list will have 1 item else no item in list)
            one_item_delete_button_list = self.request.get_all("delete_button")  # there is only 1 delete_button

            if len(one_item_delete_button_list) == 1:  # delete button is clicked
                # loop through list_of_id_checked and remove matches from db
                for an_id in list_of_id_checked:
                    # find the item with the specific id in db
                    match = BlogPost.get_by_id(int(an_id))
                    # remove the item
                    if match:
                        BlogPost.delete(match)
                time.sleep(0.7)  # to delay so db table gets displayed correct
                
            self.redirect('/edit_blog_post')
        else:
            # false user, not logged in
            self.redirect('/logout')



# '/edit_specific_blog_post', EditSpecificBlogPost
class EditSpecificBlogPost(Handler):
    def render_EditSpecificBlogPost(self, error_msg, a_headline, a_text, an_author, some_id):
        
        self.render("blog_post_edit_specific.html", error_message=error_msg, headline=a_headline, text=a_text, author_chosen=an_author, item_id=some_id)


    def get(self):
        
        the_RU = check_user_id_cookie(self.request)
            
        if the_RU:
            an_id = self.request.get("id")  # if any BlogPost headline is clicked, there is an_id
        
            if an_id:  # means there is an item to edit
                specific_item = BlogPost.get_by_id(int(an_id))  # get the item with the specific id (an_id)

                if specific_item:
                    
                    an_item_id = an_id
                    an_error_message = ""
                    # render "blog_post_edit_specific.html" with correct params!
                    self.render_EditSpecificBlogPost(an_error_message, specific_item.headline, specific_item.text, specific_item.author, an_item_id)

                else:  # no specific_item
                    self.redirect('/logout')

            else:  # no id,
                self.redirect('/logout')
            
        else:  # no the_RU
            self.redirect('/logout')
            



    def post(self):
        
        the_RU = check_user_id_cookie(self.request)
            
        # if user is correct
        if the_RU:
            an_item_id = self.request.get("item_ID")  # this is a string "455646501654613" format
##            logging.debug("an_item_id: " + an_item_id)

            if an_item_id:
                self.process_post(an_item_id)
            else:  #no an_item_id
                self.redirect('/logout')
                
        else:
            # false user, not logged in
            self.redirect('/logout')

            
    def process_post(self, an_id):        
        # data that user has entered
        headline_blog_messy = self.request.get("headline").strip()  # a string
        text_blog = self.request.get("text").strip()  # a text area...
        author_blog = self.request.get("author_blog_post") 
        
        #make sure first letter in string is upper case
        headline_blog = validation.upper_case_first_letter(headline_blog_messy)
               
        # check if all mandatory fields are filled out
        if validation.are_all_fields_filled(headline_blog, text_blog):

            # then also check if links www.xxxxx and img xxxxx.jpg has been substituted by the author
            if validation.are_xxxxx_substituted(text_blog):  # success ok to edit
                
                the_item = BlogPost.get_by_id(int(an_id))  # get the item with the specific id (an_item_id)
                        
                # update
                the_item.headline = headline_blog
                the_item.text = text_blog
                the_item.author = author_blog
                 
                the_item.put()
                time.sleep(0.7)  # to delay so db table gets displayed correct
                self.redirect("/edit_blog_post")  # tells the browser to go to '/edit_blog_post' and the response is empty

                
            else:  # xxxxx is not substituted
                # render "blog_post_edit_specific.html" and display error message and redisplay what was filled in
                self.render_EditSpecificBlogPost("Substitute the 'xxxxx'", headline_blog, text_blog, author_blog, an_id)
            
            
        else:  # not all mandatory fields are filled out
            # render "blog_post_edit_specific.html" and display error message and redisplay what was filled in
            self.render_EditSpecificBlogPost('Headline and/or Text missing', headline_blog, text_blog, author_blog, an_id)
            

        
# '/'   
class AllBlogPosts(Handler):
    def render_front(self, a_dict_blogs, an_all_blog_posts, an_older_link, a_newer_link):  # 'youngest' created date shown first by default
        
        # passing contents into the html file, NB you don't need to pass in post_parts. make_dict_blog() returns a dict
        self.render("blog_all.html", dict_bloggi = a_dict_blogs, blog_posts = an_all_blog_posts, old_link = an_older_link, new_link = a_newer_link)
        
        
    def get(self):
        POSTS_PER_PAGE = 6

        # maybe a link has been clicked!!!
        a_first_post_id = self.request.get("after_id")  # if newer posts link is clicked, there is a_first_post_id
        a_last_post_id = self.request.get("before_id")  # if older posts link is clicked, there is a_last_post_id
        
        # if there is a_first_post_id, then 'newer posts' has been clicked
        if a_first_post_id:
##            logging.debug("Goes into if: 'newer posts' has been clicked")

            # find out the post with a_first_post_id (the first post of the 3 (POSTS_PER_PAGE) shown on specific page)
            first_post = BlogPost.get_by_id(int(a_first_post_id))  # get the blogpost with the specific id (a_first_post_id)

            # check if first_post exists
            if first_post:
                # call helperfunction that returns list of posts, string for link1 and string for link2
                all_blog_posts, newer_link, older_link = dataFunctions.get_blog_posts_and_links_if_prevlink_clicked(a_first_post_id, first_post, False, "", "", True, POSTS_PER_PAGE)

            else:   # user has typed some random shit in, and first_post doesn't exist
                self.redirect('/')
                return
                
            
        # elif there is a_last_post_id, then 'older' has been clicked
        elif a_last_post_id:
##            logging.debug("Goes into else if: 'older' has been clicked")
            
            # find the post with a_last_post_id
            last_post = BlogPost.get_by_id(int(a_last_post_id))  # get the blogpost with the specific id (a_last_post_id)

            # check if last_post exists
            if last_post:
                # call helperfunction that returns list of posts, string for link1 and string for link2
                all_blog_posts, newer_link, older_link = dataFunctions.get_blog_posts_and_links_if_nextlink_clicked(a_last_post_id, last_post, False, "", "", False, POSTS_PER_PAGE)

            else:   # user has typed some random shit in, and last_post doesn't exist
                self.redirect('/')
                return

        # else, no id, then just render the very first posts
        else:
##            logging.debug("Goes into else: just display very first posts")
            all_blog_posts_plus_one = dataFunctions.find_limited_blog_posts(POSTS_PER_PAGE + 1)

            # newer_link shall never appear no matter what
            newer_link = ""
            
            # decide if older_link shall be "Older >" or ""
            older_link = validation.get_older_link(all_blog_posts_plus_one, POSTS_PER_PAGE)

            # get list of only POSTS_PER_PAGE or less
            all_blog_posts = dataFunctions.find_limited_blog_posts(POSTS_PER_PAGE)    

        self.render_front(make_dict_blog(), all_blog_posts, older_link, newer_link)



# '/full_year'
class FullYearBlogPosts (Handler):
    def render_front(self, a_list_all_year_posts, a_dict_blog, a_specific_year, an_older_link, a_newer_link):
            
        self.render("blog_entire_year.html", list_all_year_posts=a_list_all_year_posts,
                    dict_bloggi=a_dict_blog, year=a_specific_year,
                    old_link = an_older_link, new_link = a_newer_link) # passing contents into the html file

    def get(self):
        a_year = self.request.get("year")  # if any year is clicked, there is: a_year

        if a_year:   # means there is a a_year
            # turn a_year into an int
            year_integer = int(a_year)

            # from the Python package, datetime
            end_of_previous_year = datetime(year_integer - 1, 12, 31)
            start_of_next_year = datetime(year_integer + 1, 01, 01)

            POSTS_PER_PAGE = 6

            # maybe a link has been clicked!!!
            a_first_post_id = self.request.get("after_id")  # if newer posts link is clicked, there is a_first_post_id
            a_last_post_id = self.request.get("before_id")  # if older posts link is clicked, there is a_last_post_id

            if a_first_post_id:   # newer posts link is clicked, we wanna find younger posts
                # get the post with that id
                post_with_that_id = BlogPost.get_by_id(int(a_first_post_id))  # get the blogpost with the specific id (a_first_post_id)

                if post_with_that_id:
                    # call helperfunction that returns list of posts, string for link1 and string for link2
                    all_blog_posts, newer_link, older_link = dataFunctions.get_blog_posts_and_links_if_prevlink_clicked(a_first_post_id, post_with_that_id, True,
                                                                                                                        end_of_previous_year, start_of_next_year, True, POSTS_PER_PAGE)
                    
                else:   # user has typed some random shit in for id, and post_with_that_id doesn't exist
                    self.redirect('/')
                    return
                
            elif a_last_post_id:    # older posts link is clicked, we wanna find older posts
                # get the post with that id
                post_with_that_id = BlogPost.get_by_id(int(a_last_post_id))  # get the blogpost with the specific id (a_last_post_id)

                if post_with_that_id:
                    # call helperfunction that returns list of posts, string for link1 and string for link2
                    all_blog_posts, newer_link, older_link = dataFunctions.get_blog_posts_and_links_if_nextlink_clicked(a_last_post_id, post_with_that_id, True,
                                                                                                                        end_of_previous_year, start_of_next_year, False, POSTS_PER_PAGE)

                else:   # user has typed some random shit in for id, and post_with_that_id doesn't exist
                    self.redirect('/')
                    return

            else:    # neither newer or older link has been clicked. This is the year link that has been clicked
                # newer_link shall never appear no matter what
                newer_link = ""
                
                # decide if older_link shall be "Older >" or ""
                all_blog_posts_plus_one = dataFunctions.find_blog_posts_between(POSTS_PER_PAGE + 1, end_of_previous_year, start_of_next_year)
##                logging.debug("in year: length of all_blog_posts_plus_one = " + str(len(all_blog_posts_plus_one)))
                older_link = validation.get_older_link(all_blog_posts_plus_one, POSTS_PER_PAGE)
            
                # find blog posts for this specific year, get list of only POSTS_PER_PAGE or less
                all_blog_posts = dataFunctions.find_blog_posts_between(POSTS_PER_PAGE, end_of_previous_year, start_of_next_year)

            if len(all_blog_posts) < 1:   # nothing to display, checks if user just type in a random year that doesn't exist in menu yet
                self.redirect('/')
            else:   
                self.render_front(all_blog_posts, make_dict_blog(), a_year, older_link, newer_link)

        else:   # nothing to display cause no a_year 
            self.redirect('/')           



# '/full_month'
class FullMonthBlogPosts (Handler):
    def render_front(self, a_list_all_month_posts, a_dict_blog):
        
        self.render("blog_entire_month.html", list_all_month_posts=a_list_all_month_posts, dict_bloggi=a_dict_blog) # passing contents into the html file


    def get(self):
        a_year_and_month = self.request.get("year_and_month")  # if any year is clicked, there is: a_year_and_month
        just_year = a_year_and_month[0:4]
        just_month = a_year_and_month[4:]  # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, or 12

        # make month to format 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, or 12
        if len(just_month) < 2:
            just_month = '0' + just_month

        # find all blogposts
        all_blog_posts = dataFunctions.find_all_blog_posts()    
        
        only_specific_month = []  # list to contain blogposts

        if a_year_and_month:   # means there is a a_year_and_month
            for posts in all_blog_posts:
                if validation.get_just_yyyy(posts.created) == just_year:  # we only want blog posts that is from for example 2014
                    # we only want blog posts that is from for example year 2014 AND from for example month 05
                    if validation.get_just_mm(posts.created) == just_month:
                        only_specific_month.append(posts)
            if len(only_specific_month) < 1:  # nothing to display
                self.redirect('/')
            else:
                self.render_front(only_specific_month, make_dict_blog())

        else:   # nothing to display
            self.redirect('/')



# '/single_blog_post'     
class SingleBlogPost(Handler):
    def render_front(self, a_single_blog_posts, a_dict_blog):
            
        self.render("blog_single_post.html",  single_blog_posts=a_single_blog_posts,
                    dict_bloggi=a_dict_blog) # passing contents into the html file


    def get(self):        
        blog_post_id = self.request.get("single_post_id")  # if any single blog post is clicked, there is: blog_post_id (format string)
        
        if blog_post_id:  # means there is a blog_post_id
##            logging.debug("goes into if statement")
            specific_blog_post = BlogPost.get_by_id(int(blog_post_id))  # get the specific_blog_post with the specific id (blog_post_id)
            if specific_blog_post:
                self.render_front(specific_blog_post, make_dict_blog())
            else:
##                logging.debug("goes into first else statement")
                self.redirect('/')
                
        else:  # no blog post
##            logging.debug("goes into else statement")
            self.redirect('/')



# '/add_photo'    
class AddPhoto(Handler):
    def render_AddPhoto(self, error_msg, an_img_format, an_img, a_txt_below):
        
        self.render("photos_add_photo.html", error_message=error_msg, img_format=an_img_format, img=an_img, txt_below_img=a_txt_below)

 
    def get(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.render_AddPhoto("", "", "", "")
        else:
            # false user, not logged in
            self.redirect('/')


    def post(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.process_add_photo()
        else:
            # false user, not logged in
            self.redirect('/')


    def process_add_photo(self):            
        # data that user has entered
        L_P_photo = self.request.get("L_or_P_img").strip()  # a string 
        img_file = self.request.get("img_file").strip()  # a string
        text_below_img = self.request.get("text_below_img").strip()  # a string

        if validation.are_format_and_img_file_and_text_filled_correct(L_P_photo, img_file, text_below_img):
            # process by creating Photo item in db
            photo = Photo(img_format = L_P_photo, img = img_file, txt_below_img=text_below_img)
            photo.put()
            
            #display blank page, render "photos_add_photo.html"!
            self.render_AddPhoto("", "", "", "")

        else:   # not all mandatory fields filled out, so don't process - instead redisplay page            
            # render "photos_add_photo.html" and display error message and redisplay what was filled in
            self.render_AddPhoto('Mandatory field(s) either missing or wrong', L_P_photo, img_file, text_below_img)



# '/photos'   
class AllPhotos(Handler):
    def render_front(self, a_headline, a_list, dict_for_blog_archive):  # 'youngest' created date shown first by default
        # passing contents into the html file
        self.render("photos_main.html", headline_photos=a_headline, image_list=a_list, dict_bloggi=dict_for_blog_archive)
        

    def get(self):
        ##### Decision: show all photos on one page. cause centering looks stupid when user resize the page.#####

        # get list of all photos
        all_photos = dataFunctions.find_all_photos()
        
        logging.debug("length of all_photos = " + str(len(all_photos)))

##        logging.debug("length of all_photos = " + str(len(all_photos)))

        # check if there are any img's to show in gallery
        if len(all_photos) < 1:
            # no images so pass in an empty list
            photo_list = []
            self.render_front("Sorry - Photo gallery is empty", photo_list, make_dict_blog())
        else:
            # call function that organizes the rows and returns a list of lists
            #photo_all_rows_list = dataFunctions.get_rows_of_photos_list_of_list(all_photos, MAX_IMG_ON_ROW_DECIMAL, MAX_IMG_ON_ROW_INT)
                        
            self.render_front("Click photo to enlarge - click again to close", all_photos, make_dict_blog())
            






        

##        ROWS_PER_PAGE = 5  # constant to decide the max rows to show per page
##        
##        MAX_IMG_ON_ROW_INT = 7
##
##        MAX_IMG_ON_ROW_DECIMAL = 7.0

##        MAX_IMG_PER_PAGE = 21

        

##        # maybe a link has been clicked!!!
##        a_first_photo_id = self.request.get("after_id")  # if previous link is clicked, there is a_first_photo_id
##        a_last_photo_id = self.request.get("before_id")  # if next link is clicked, there is a_last_photo_id
##
##        # if there is a_first_photo_id, then 'previous' has been clicked
##        if a_first_photo_id:
####            logging.debug("Goes into if: 'previous' has been clicked")
##
##            # find out the photo with a_first_photo_id (the first photo of the 3 (ROWS_PER_PAGE) shown on specific page)
##            first_photo = Photo.get_by_id(int(a_first_photo_id))  # get the blogpost with the specific id (a_first_photo_id)
##
##            # check if first_photo exists
##            if first_photo:
##                # call helperfunction that returns list of photos, string for link1 and string for link2
##                all_photos, newer_link, older_link = dataFunctions.get_posts_and_links_if_prevlink_clicked(first_photo, True, True, MAX_IMG_PER_PAGE)
##
##            else:   # user has typed some random shit in
##                self.redirect('/photos')
##                return
##
##        # elif there is a_last_photo_id, then 'next' has been clicked
##        elif a_last_photo_id:
####            logging.debug("Goes into else if: 'next' has been clicked")
##            
##            # find out the photo with a_last_photo_id
##            last_photo = Photo.get_by_id(int(a_last_photo_id))  # get the photo with the specific id (a_last_photo_id)
##
##            # check if last_photo exists
##            if last_photo:
##
##                # call helperfunction that returns list of photos, string for link1 and string for link2
##                all_photos, newer_link, older_link = dataFunctions.get_posts_and_links_if_nextlink_clicked(last_photo, True, False, MAX_IMG_PER_PAGE)
##                
##            else:   # user has typed some random shit in
##                self.redirect('/photos')
##                return
##
##        # else, no id, then just render the very first photos
##        else:
####            logging.debug("Goes into else: just display very first photos")
##            all_photos_plus_one = dataFunctions.find_limited_photos(MAX_IMG_PER_PAGE + 1)
##            
##            logging.debug("length of all_photos_plus_one = " + str(len(all_photos_plus_one)))
##
##            # newer_link shall never appear no matter what
##            newer_link = ""
##            
##            # decide if older_link shall be "Next >" or ""
##            older_link = validation.get_next_link(all_photos_plus_one, MAX_IMG_PER_PAGE)
##
##            # get list of only ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT or less
##            all_photos = dataFunctions.find_limited_photos(MAX_IMG_PER_PAGE)
##            
##            logging.debug("length of all_photos = " + str(len(all_photos)))
##
####        logging.debug("length of all_photos = " + str(len(all_photos)))
##
##        # check if there are any img's to show in gallery
##        if len(all_photos) < 1:
##            # no images so pass in an empty list
##            photo_all_rows_list = []
##            self.render_front("Sorry - Photo gallery is empty", photo_all_rows_list, newer_link, older_link)
##        else:
##            # call function that organizes the rows and returns a list of lists
##            #photo_all_rows_list = dataFunctions.get_rows_of_photos_list_of_list(all_photos, MAX_IMG_ON_ROW_DECIMAL, MAX_IMG_ON_ROW_INT)
##                        
##            self.render_front("Click photo to enlarge - click again to close", all_photos, newer_link, older_link)







# '/add_video'    
class AddVideo(Handler):
    def render_AddVideo(self, error_msg, an_iframe_tag_input):
        
        self.render("videos_add_video.html", error_message=error_msg, iframe_tag_input=an_iframe_tag_input)


    def get(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.render_AddVideo("", "")
        else:
            # false user, not logged in
            self.redirect('/')


    def post(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.process_add_video()
        else:
            # false user, not logged in
            self.redirect('/')


    def process_add_video(self):            
        # data that user has entered
        the_iframe_tag = self.request.get("iframe_tag").strip()  # a string

        if validation.is_there_a_tag(the_iframe_tag):

            # is tag valid
            if validation.are_xxxxx_replaced(the_iframe_tag):
                # process by creating Video item in db
                video = Video(iframe_tag_and_content = the_iframe_tag)
                video.put()
                
                #display blank page
                # render "videos_add_video.html"!
                self.render_AddVideo("", "")
            else:
                # display error message
                # don't process - instead redisplay page
                # render "videos_add_photo.html" and display error message and redisplay what was filled in  (delete previous tag or else it screws page up).
                self.render_AddVideo('Replace xxxxx with iframe tag', "")

        else:
            # don't process - instead redisplay page
            
            # not all mandatory fields filled out
            # render "videos_add_photo.html" and display error message and redisplay what was filled in (which will be empty string in this case)
            self.render_AddVideo('Mandatory field is missing', the_iframe_tag)


            
# '/videos'   
class AllVideos(Handler):
    def render_front(self, a_headline, an_all_videos, a_previous_link, a_next_link, dict_for_blog_archive):
        # passing contents into the html file
        self.render("videos_main.html", headline_videos=a_headline, video_list=an_all_videos,
                    new_link = a_previous_link, old_link = a_next_link, dict_bloggi=dict_for_blog_archive)
        

    def get(self):
        
        headline="Videos"

        VIDEOS_PER_PAGE = 10

        # maybe a link has been clicked!!!
        a_first_video_id = self.request.get("after_id")  # if Previous link is clicked, there is a_first_video_id
        a_last_video_id = self.request.get("before_id")  # if Next link is clicked, there is a_last_video_id
        
        # if there is a_first_video_id, then 'Previous' has been clicked
        if a_first_video_id:
##            logging.debug("Goes into if: 'Previous' has been clicked")

            # find out the video with a_first_video_id (the first video of the 3 (VIDEOS_PER_PAGE) shown on specific page)
            first_video = Video.get_by_id(int(a_first_video_id))  # get the video with the specific id (a_first_video_id)

            # check if first_video exists
            if first_video:
                # call helperfunction that returns list of videos, string for link1 and string for link2
                all_videos, newer_link, older_link = dataFunctions.get_posts_and_links_if_prevlink_clicked(first_video, False, True, VIDEOS_PER_PAGE)


            else:   # user has typed some random shit in
                self.redirect('/videos')
                return
                
        # elif there is a_last_video_id, then 'Next' has been clicked
        elif a_last_video_id:
##            logging.debug("Goes into else if: 'Next' has been clicked")
            
            # find out the video with a_last_video_id
            last_video = Video.get_by_id(int(a_last_video_id))  # get the video with the specific id (a_last_video_id)

            # check if last_video exists
            if last_video:
                # call helperfunction that returns list of photos, string for link1 and string for link2
                all_videos, newer_link, older_link = dataFunctions.get_posts_and_links_if_nextlink_clicked(last_video, False, False, VIDEOS_PER_PAGE)

            else:   # user has typed some random shit in
                self.redirect('/videos')
                return

        # else, no id, then just render the very first videos
        else:
##            logging.debug("Goes into else: just display very first videos")
            all_videos_plus_one = db.GqlQuery("SELECT * FROM Video ORDER BY created DESC").fetch(VIDEOS_PER_PAGE+1)

            # previous_link shall never appear no matter what
            newer_link = ""
            
            # decide if next_link shall be "Next >" or ""
            older_link = validation.get_next_link(all_videos_plus_one, VIDEOS_PER_PAGE)

            # only get list of 3 or less
            all_videos = db.GqlQuery("SELECT * FROM Video ORDER BY created DESC").fetch(VIDEOS_PER_PAGE)
##            logging.debug("lenght all_videos = " + str(len(all_videos)))

            if len(all_videos) < 1:
                headline="Sorry - no videos"
        
        self.render_front(headline, all_videos, newer_link, older_link, make_dict_blog())



  
# '/about', AboutUs
class AboutUs(Handler):
    def get(self):
        dict_for_blog_archive = make_dict_blog()
        self.render("about.html", dict_bloggi=dict_for_blog_archive)

        
        
# '/contact', ContactUs
class ContactUs(Handler):
    def render_contact_us(self, submission_cont,
                          name, name_error,
                          email, email_error,
                          message, message_error,
                          dict_for_blog_archive):
        
        self.render("contact.html", submission_content=submission_cont,
                    user_name_content=name , user_name_error=name_error,
                    user_email_content=email, user_email_error=email_error,
                    user_message_content=message, user_message_error=message_error,
                    dict_bloggi=dict_for_blog_archive)

        
    def get(self):
        self.render_contact_us("", "", "", "", "", "", "", make_dict_blog())


    def post(self):
        # check if valid username

        username_input = self.request.get("user_name")
        user_email_input = self.request.get("user_email").strip()
        user_message_input = self.request.get("user_message")  # textarea

        # check if all fields are filled out and get the error messages
        all_fields_filled, name_error, email_error, message_error = validation.are_all_contact_fields_filled(username_input, user_email_input, user_message_input)

        if all_fields_filled:
            
##            logging.debug("Email is SEND")

            # send user_message_input to email blogkirstine@gmail.com
            emailFunctions.sendEmail(username_input, user_email_input, user_message_input)

            self.redirect('/contact_success')

        # else
        else:  # not all fields filled out
            
##            logging.debug("Email NOT send")
            
            self.render_contact_us("Sorry, something went wrong  -  check the fields below", 
                                   username_input, name_error,
                                   user_email_input, email_error,
                                   user_message_input, message_error,
                                   make_dict_blog())
        

        
# '/contact_success', ContactUsSuccess
class ContactUsSuccess(Handler):
    def render_success(self, submission_cont, dict_for_blog_archive):
        
        self.render("contact_success.html", submission_content=submission_cont, dict_bloggi=dict_for_blog_archive)

        
    def get(self):
        
        self.render_success("Thank you  -  your message has been sent", make_dict_blog())


    
app = webapp2.WSGIApplication([('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/add_blog_post', AddNewBlogPost),
                               ('/edit_blog_post', EditBlogPost),
                               ('/edit_specific_blog_post', EditSpecificBlogPost),
                               ('/', AllBlogPosts),
                               ('/full_year', FullYearBlogPosts),
                               ('/full_month', FullMonthBlogPosts),
                               ('/single_blog_post', SingleBlogPost),
                               ('/add_photo', AddPhoto),
                               ('/photos', AllPhotos),
                               ('/add_video', AddVideo),
                               ('/videos', AllVideos),
                               ('/about', AboutUs),
                               ('/contact', ContactUs),
                               ('/contact_success', ContactUsSuccess)], debug=True)

            
## ('/add_user', AddUserHandler)
