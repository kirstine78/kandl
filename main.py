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
        # if user is correct
        if True:
            #display blank page
            self.render_blank_blog_post()
            
        #else

    def post(self):
        # data that user has entered
        headline_blog_messy = self.request.get("headline").strip()  # a string
        text_blog = self.request.get("text").strip()  # a text area...
		
        #make sure first letter in string is upper case
        headline_blog = validation.upper_case_first_letter(headline_blog_messy)
        
        
        # create BlogPost item in db
        bp = BlogPost(headline = headline_blog, text = text_blog)
                      
                      
       
        #time.sleep(0.5)  # to delay so db table gets displayed correct

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

        
        
class AllBlogPosts(Handler):
    def render_front(self):  # 'youngest' created date shown first by default
        all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(1000)

        dict_blog = {}  # {'2014':{'12':['p1', 'p2', 'p3'], '11':['p4', 'p5'], '8':['p6', 'p7']}, '2013':{'12':['p8', 'p9'], '8':['p1', 'p2']}}

                            

        for blog_posts in all_blog_posts:
            a_year = validation.get_just_yyyy(blog_posts.created)  # get string yyyy
            a_month = str(int(validation.get_just_mm(blog_posts.created)))  # get string mm and make the format 1,2,3,4,5,6,7,8,9,10,11,12

            if a_year not in dict_blog:
                dict_blog[a_year] = {} # add a_year as key to the dict with empty dict as value

                
                if a_month not in dict_blog[a_year]:  # a_month not a key in inner dict for that year
                    
                    # make a_month a key with empty list as value
                    dict_blog[a_year][a_month] = []

                    # append headline to the list
                    dict_blog[a_year][a_month].append(blog_posts.headline)


                else:
                    # append headline to the list
                    dict_blog[a_year][a_month].append(blog_posts.headline)

            else:
                if a_month not in dict_blog[a_year]:  # a_month not a key in inner dict for that year
                    
                    # make a_month a key with empty list as value
                    dict_blog[a_year][a_month] = []

                    # append headline to the list
                    dict_blog[a_year][a_month].append(blog_posts.headline)


                else:
                    # append headline to the list
                    dict_blog[a_year][a_month].append(blog_posts.headline)

        
        #logging.debug("DICT BLOG = " + dict_blog['2014']['6'][0])
        
        # passing contents into the html file, nb you don't need to pass in post_parts
        self.render("blog_all.html", dict_bloggi = dict_blog, blog_posts = all_blog_posts) 
        

    def get(self):
        self.render_front()


    def post(self):
        self.render_front()


    
class SingleBlogPost(Handler):
    def render_front(self, single_headline, single_date, single_text, single_img_a, single_text_below):
            
        self.render("blog_single.html",  specific_headline=single_headline,
                    specific_date=single_date , specific_text=single_text,
                    specific_img_a=single_img_a, specific_txt_below=single_text_below) # passing contents into the html file

    def get(self):
        blog_post_id = self.request.get("id")  # if any blog post (either little img, headline or text) is clicked, there is: blog_post_id
        if blog_post_id:  # means there is a blog_post
            specific_blog_post = BlogPost.get_by_id(int(blog_post_id))  # get the blog_post with the specific id (blog_post_id)
            a_headline = specific_blog_post.headline
            a_date = validation.convert_to_letter_month(specific_blog_post.created)
            a_text = specific_blog_post.text
            an_img_a = specific_blog_post.img_a
            a_text_below = specific_blog_post.txt_below
        else:  # no blog post
            a_headline = ""
            a_date = ""
            a_text = ""
            an_img_a = ""
            a_text_below = ""

            
        self.render_front(a_headline, a_date, a_text, an_img_a, a_text_below)


##    def post(self):
##        self.render_front()


class AboutUs(Handler):
    def get(self):
        self.render("about.html")
        



app = webapp2.WSGIApplication([('/add_blog_post', AddNewBlogPost),
                               ('/', AllBlogPosts),
                               ('/single_blog_post', SingleBlogPost),
                               ('/about', AboutUs)], debug=True)



    
##app = webapp2.WSGIApplication([('/add_blog_post', AddNewBlogPost),
##                               ('/', Home),
##                               ('/all_blog_posts', AllBlogPosts),
##                               ('/single_blog_post', SingleBlogPost),
##                               ('/about', AboutUs),
##                               ('/blog_overview', BlogOverview)], debug=True)



            
##        
##class Home(Handler):
##    def render_front(self):  # 'youngest' created date shown first by default
##        # find the newest 5 posts
##        all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC limit 5").fetch(5)
##            
##        self.render("home.html", blog_posts = all_blog_posts) # passing contents into the html file
##
##    def get(self):
##        self.render_front()
##
##
##    def post(self):
##        self.render_front()


    
##class BlogOverview(Handler):
##    def get(self):
##        # find all posts
##        all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(1000)
##
##        # passing contents into the html file
##        self.render("blog_overview.html", blog_posts = all_blog_posts) 
