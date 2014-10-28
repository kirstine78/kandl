#!/usr/bin/env python
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

import validation
import passwordValid
import dataFunctions
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


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
jinja_env.globals.update(format_the_date=validation.convert_to_letter_month)  # lets me use validation inside html.
jinja_env.globals.update(numeric_to_alphabetic_month=validation.numeric_to_alpabetic)  # lets me use validation inside html.


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

    created = db.DateTimeProperty(auto_now_add = True)  # more precise date, when sorting with format yyyy-mm-dd 06:46:22.467000
    _string_date_new = ""


class PostPart(db.Model):  # abbreviated 'pp'
    parent_blog_post = db.ReferenceProperty(BlogPost, collection_name='post_parts')   # ReferenceProperty reference to another db.Model
    
    img_format = db.StringProperty(required = False)
    img = db.StringProperty(required = False)
    txt_below_img = db.StringProperty(required = False)


class RegisteredUsers(db.Model):  #  --> ru
    name = db.StringProperty(required = True)
    password_hashed = db.StringProperty(required = True)  # (name + pw + salt) hexdigested and then pipe salt with format "hexdigestedValue|salt"
    created = db.DateTimeProperty(auto_now_add = True)


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

def make_dict_blog(collection_of_blog_posts):
    """Takes a collection of blogposts (from db) and return a dictionary
        with format example:
        {'2014':{'12':['p1', 'p2', 'p3'], '11':['p4', 'p5'], '8':['p6', 'p7']}, '2013':{'12':['p8', 'p9'], '8':['p1', 'p2']}}
        """
    
    all_blog_posts = collection_of_blog_posts
    
    dictionary = {}  # {'2014':{'12':['p1', 'p2', 'p3'], '11':['p4', 'p5'], '8':['p6', 'p7']}, '2013':{'12':['p8', 'p9'], '8':['p1', 'p2']}}

    for blog_posts in all_blog_posts:
        a_year = validation.get_just_yyyy(blog_posts.created)  # get string yyyy
        a_month = str(int(validation.get_just_mm(blog_posts.created)))  # get string mm and make the format 1,2,3,4,5,6,7,8,9,10,11,12

        if a_year not in dictionary:
            dictionary[a_year] = {} # add a_year as key to the dict with empty dict as value

            
            if a_month not in dictionary[a_year]:  # a_month not a key in inner dict for that year
                
                # make a_month a key with empty list as value
                dictionary[a_year][a_month] = []

                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_posts)


            else:
                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_posts)

        else:
            if a_month not in dictionary[a_year]:  # a_month not a key in inner dict for that year
                
                # make a_month a key with empty list as value
                dictionary[a_year][a_month] = []

                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_posts)


            else:
                # append specific blogpost to the list
                dictionary[a_year][a_month].append(blog_posts)
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

        #then redirect to '/login' LoginHandler
        self.redirect("/login")



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
    def render_AddNewBlogPost(self, error_msg, bp_db, a_pp_list):
        
        self.render("blog_post_entry.html", error_message=error_msg, bp=bp_db, pp_list=a_pp_list)

    def render_blank_blog_post(self):
        # create BlogPost item in db
        bp = BlogPost(headline = "", text = "")

        post_parts_list = []
        
        for i in range(1,5,1):
        

            pp = PostPart(img_format = "",
                          img = "",
                          txt_below_img = "")

            post_parts_list.append(pp)
        
        # render "blog_post_entry.html" with correct params!
        self.render_AddNewBlogPost("", bp, post_parts_list)

 
    def get(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.render_blank_blog_post()
        else:
            # false user, not loged in
            self.redirect('/')


    def post(self):
        the_RU = check_user_id_cookie(self.request)
        
        # if user is correct
        if the_RU:
            self.process_post()
        else:
            # false user, not loged in
            self.redirect('/')


    def process_post(self):            
        # data that user has entered
        headline_blog_messy = self.request.get("headline").strip()  # a string
        text_blog = self.request.get("text").strip()  # a text area...
		
        #make sure first letter in string is upper case
        headline_blog = validation.upper_case_first_letter(headline_blog_messy)
        
        
        # create BlogPost item in db
        bp = BlogPost(headline = headline_blog, text = text_blog)
        

        #logging.debug("bp.text = " + bp.text)

        # list for all post parts
        blog_post_parts_list = []
        
        # if different amount of img's is needed then change the second paramter
        for i in range(0,4,1):
            
            L_P_blog = self.request.get("L_or_P_img"+str(i)).strip()  # a string
            img_blog = self.request.get("img"+str(i)).strip()  # a string
            text_below_img_blog = self.request.get("text_below_img"+str(i)).strip()  # a string

            
            # create PostPart item in db
            pp = PostPart(img_format = L_P_blog,
                          img = img_blog,
                          txt_below_img = text_below_img_blog)

            blog_post_parts_list.append(pp)
        
        

        #logging.debug("bp.string_date = " + bp.string_date)
        

        # check if all mandatory fields are filled out
        if validation.are_all_fields_filled(headline_blog, text_blog):
            bp.put()

            # can't do the below before bp is put()
            for post_part in blog_post_parts_list:
                post_part.parent_blog_post = bp
                post_part.put()

            #display blank page
            # render "blog_post_entry.html"!
            self.render_blank_blog_post()
            
        else:  # not all mandatory fields filled out
            # render "blog_post_entry.html" and display error message and redisplay what was filled in
            self.render_AddNewBlogPost('Headline and/or Text missing', bp, blog_post_parts_list)


        
# '/'   
class AllBlogPosts(Handler):
    def render_front(self):  # 'youngest' created date shown first by default
        all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(1000)

        #dict_blog = {}  # {'2014':{'12':['p1', 'p2', 'p3'], '11':['p4', 'p5'], '8':['p6', 'p7']}, '2013':{'12':['p8', 'p9'], '8':['p1', 'p2']}}
        dict_blog = make_dict_blog(all_blog_posts)

        #logging.debug("DICT BLOG = " + dict_blog['2014']['6'][0])
        
        # passing contents into the html file, nb you don't need to pass in post_parts
        self.render("blog_all.html", dict_bloggi = dict_blog, blog_posts = all_blog_posts) 
        

    def get(self):
        self.render_front()


    def post(self):
        self.render_front()



# '/full_year'
class FullYearBlogPosts (Handler):
    def render_front(self, a_list_all_year_posts, a_dict_blog):
            
        self.render("blog_entire_year.html", list_all_year_posts=a_list_all_year_posts, dict_bloggi=a_dict_blog) # passing contents into the html file

    def get(self):
        year_id = self.request.get("id")  # if any year is clicked, there is: year_id
        
        all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(1000)
        dict_blog = make_dict_blog(all_blog_posts)  # we need this to display the menu in the html
        
        logging.debug("year_id = " + year_id)
        
        only_specific_year = []  # list to contain blogposts

        if year_id:   # means there is a year_id
            
            for posts in all_blog_posts:
                if validation.get_just_yyyy(posts.created) == year_id:  # we only want blog posts that is from for example 2014
                    only_specific_year.append(posts)
        
        self.render_front(only_specific_year, dict_blog)

      

# '/full_month'
class FullMonthBlogPosts (Handler):
    def render_front(self, a_list_all_month_posts, a_dict_blog):
            
        self.render("blog_entire_month.html", list_all_month_posts=a_list_all_month_posts, dict_bloggi=a_dict_blog) # passing contents into the html file

    def get(self):
        year_and_month_id = self.request.get("id")  # if any year is clicked, there is: year_and_month_id
        just_year = year_and_month_id[0:4]
        just_month = year_and_month_id[4:]  # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, or 12

        # make month to format 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, or 12
        if len(just_month) < 2:
            just_month = '0' + just_month
        
        all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(1000)
        dict_blog = make_dict_blog(all_blog_posts)  # we need this to display the menu in the html
        
##        logging.debug("year_and_month_id = " + year_and_month_id)
##        logging.debug("just_year = " + just_year)
##        logging.debug("just_month = " + just_month)
        
        only_specific_month = []  # list to contain blogposts

        if year_and_month_id:   # means there is a year_and_month_id
            for posts in all_blog_posts:
                if validation.get_just_yyyy(posts.created) == just_year:  # we only want blog posts that is from for example 2014
                    # we only want blog posts that is from for example year 2014 AND from for example month 05
                    if validation.get_just_mm(posts.created) == just_month:
                        only_specific_month.append(posts)
        
        self.render_front(only_specific_month, dict_blog)

      





# '/single_blog_post'     
class SingleBlogPost(Handler):
    def render_front(self, a_single_blog_posts, a_dict_blog):
            
        self.render("blog_single_post.html",  single_blog_posts=a_single_blog_posts,
                    dict_bloggi=a_dict_blog) # passing contents into the html file

    def get(self):
        all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(1000)
        dict_blog = make_dict_blog(all_blog_posts)  # we need this to display the menu bar in the html
        
        blog_post_id = self.request.get("id")  # if any single blog post is clicked, there is: blog_post_id (format string)
        
        if blog_post_id:  # means there is a blog_post
            specific_blog_post = BlogPost.get_by_id(int(blog_post_id))  # get the specific_blog_post with the specific id (blog_post_id)
        else:  # no blog post
            self.redirect('/')

            
        self.render_front(specific_blog_post, dict_blog)



class AboutUs(Handler):
    def get(self):
        self.render("about.html")
        



app = webapp2.WSGIApplication([('/add_blog_post', AddNewBlogPost),
                               ('/', AllBlogPosts),
                               ('/about', AboutUs),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/full_year', FullYearBlogPosts),
                               ('/full_month', FullMonthBlogPosts),
                               ('/single_blog_post', SingleBlogPost)], debug=True)




                               


