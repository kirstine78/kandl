def b(self):
    all_blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC").fetch(1000)

    dict_blog = {}  # {'2014':{'dec':['p1', 'p2', 'p3'], 'nov':['p4', 'p5'], 'aug':['p6', 'p7']}, '2013':{'dec':['p8', 'p9'], 'aug':['p1', 'p2']}}
    
    
    all_years = []  # list containing strings
           
    months_specific_year = []

    posts_specific_month = []



##        for blog_posts in all_blog_posts:
##            a_year = validation.get_just_yyyy(blog_posts.created)  # get string yyyy
##
##            
##            if a_year not in dict_blog:
##                dict_blog[a_year] = {} # add a_year as key to the dict with empty dict as value
                


    for blog_posts in all_blog_posts:
        a_year = validation.get_just_yyyy(blog_posts.created)  # get string yyyy
        a_month = validation.get_just_mm(blog_posts.created)  # get string mm

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

