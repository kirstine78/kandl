# Helper to get list of blogposts and newer older links for BlogPost
def get_blog_posts_and_links(an_id, a_post, are_there_between_factor, an_end_of_previous_year, a_start_of_next_year, max_posts_per_page):
""" boolean are_there_between_factor """

### get the post with that id an_id
##a_post = BlogPost.get_by_id(int(an_id))  # get the blogpost with the specific id (an_id)
   

if are_there_between_factor:  # are_there_between_factor True  (for FullYear)

    # decide if newer_link shall be "< Newer posts" or ""
    all_blog_posts_plus_one = find_blog_posts_between_and_younger(max_posts_per_page + 1, an_end_of_previous_year, a_start_of_next_year, an_id)
##                logging.debug("length of all_blog_posts_plus_one = " + str(len(all_blog_posts_plus_one)))

    # get list of only max_posts_per_page or less
    all_blog_posts = find_blog_posts_between_and_younger(max_posts_per_page, end_of_previous_year, start_of_next_year, an_id)

    
else:   # are_there_between_factor False  (AllBlogPosts)
    # find out the created date of the post with an_id
    created_post = a_post.created

    # if 'newer posts' has been clicked we know that there are at least max_posts_per_page posts to show
    # find the younger posts to be shown
    all_blog_posts_plus_one = find_newer_blog_posts(max_posts_per_page + 1, created_post)
    
##            logging.debug("length of all_blog_posts_plus_one = " + str(len(all_blog_posts_plus_one)))

    # get list of only max_posts_per_page or less
    all_blog_posts = dataFunctions.find_newer_blog_posts(max_posts_per_page, created_post)


# reverse, cause you get ASC and you want DESC
all_blog_posts.reverse()

# decide if newer_link shall be "< Newer posts" or ""
newer_link = validation.get_newer_link(all_blog_posts_plus_one, max_posts_per_page)

# older_link shall appear no matter what
older_link = "Older posts &#9658;"

return all_blog_posts, newer_link, older_link



    
##else:   # are_there_between_factor True
##
##    # check if a_post exists
##    if a_post:
##        # find out the created date of the post with an_id
##        created_post = a_post.created
##        
##    ##            logging.debug("created_post = " + str(created_post))
##
##        # if 'newer posts' has been clicked we know that there are at least max_posts_per_page posts to show
##        # find the younger posts to be shown
##        all_blog_posts_plus_one = find_newer_blog_posts(max_posts_per_page + 1, created_post)
##        
##    ##            logging.debug("length of all_blog_posts_plus_one = " + str(len(all_blog_posts_plus_one)))
##
##        # older_link shall appear no matter what
##        older_link = "Older posts &#9658;"
##
##        # decide if newer_link shall be "< Newer posts" or ""
##        newer_link = validation.get_newer_link(all_blog_posts_plus_one, max_posts_per_page)
##
##        # get list of only max_posts_per_page or less
##        all_blog_posts = dataFunctions.find_newer_blog_posts(max_posts_per_page, created_post)
##
##        # revers the list
##        all_blog_posts.reverse()
##
##    else:   # user has typed some random shit in, and first_post doesn't exist
##        self.redirect('/')
##        return
        


    
##all_whatever_kind_plus_one = 
##older_link = "Older posts &#9658;"
##    
###Photo and Video
##if it is Post or Video:
##    older_link = "Next &#9658;"


##########      AllBlogPosts        #######################

# if there is a_first_post_id, then 'newer posts' has been clicked
        if a_first_post_id:
##            logging.debug("Goes into if: 'newer posts' has been clicked")

            # find out the post with a_first_post_id (the first post of the 3 (POSTS_PER_PAGE) shown on specific page)
            first_post = BlogPost.get_by_id(int(a_first_post_id))  # get the blogpost with the specific id (a_first_post_id)

            # check if first_post exists
            if first_post:
                # find out the created date of the post with a_first_post_id
                created_first_post = first_post.created
                
                # to avoid: BadQueryError: Type Cast Error: unable to cast ['2014-11-11 18:09:25.495000'] with operation DATETIME (unconverted data remains: .495000)            
                #created_first_post = created_first_post[0:19]
                
    ##            logging.debug("created_first_post = " + str(created_first_post))

                # if 'newer posts' has been clicked we know that there are at least POSTS_PER_PAGE posts to show
                # find the younger posts to be shown
                all_blog_posts_plus_one = dataFunctions.find_newer_blog_posts(POSTS_PER_PAGE + 1, created_first_post)
                
    ##            logging.debug("length of all_blog_posts_plus_one = " + str(len(all_blog_posts_plus_one)))

                # older_link shall appear no matter what
                older_link = "Older posts &#9658;"

                # decide if newer_link shall be "< Newer posts" or ""
                newer_link = validation.get_newer_link(all_blog_posts_plus_one, POSTS_PER_PAGE)

                # get list of only POSTS_PER_PAGE or less
                all_blog_posts = dataFunctions.find_newer_blog_posts(POSTS_PER_PAGE, created_first_post)

                # revers the list
                all_blog_posts.reverse()

            else:   # user has typed some random shit in, and first_post doesn't exist
                self.redirect('/')
                return


##########      FullYearBlogPosts        #######################

        if a_first_post_id:   # newer posts link is clicked, we wanna find younger posts

            # get the post with that id
            post_with_that_id = BlogPost.get_by_id(int(a_first_post_id))  # get the blogpost with the specific id (a_first_post_id)

            if post_with_that_id:

                # older_link shall appear no matter what
                older_link = "Older posts &#9658;"

                # decide if newer_link shall be "< Newer posts" or ""
                all_blog_posts_plus_one = dataFunctions.find_blog_posts_between_and_younger(POSTS_PER_PAGE + 1, end_of_previous_year, start_of_next_year, a_first_post_id)
##                logging.debug("length of all_blog_posts_plus_one = " + str(len(all_blog_posts_plus_one)))
                newer_link = validation.get_newer_link(all_blog_posts_plus_one, POSTS_PER_PAGE)

                # get list of only POSTS_PER_PAGE or less
                all_blog_posts = dataFunctions.find_blog_posts_between_and_younger(POSTS_PER_PAGE, end_of_previous_year, start_of_next_year, a_first_post_id)

                # reverse, cause you get ASC and you want DESC
                all_blog_posts.reverse()

            else:   # user has typed some random shit in for id, and post_with_that_id doesn't exist
                self.redirect('/')
                return


##########      AllPhotos        #######################
            
# if there is a_first_photo_id, then 'previous' has been clicked
        if a_first_photo_id:
##            logging.debug("Goes into if: 'previous' has been clicked")

            # find out the photo with a_first_photo_id (the first photo of the 3 (ROWS_PER_PAGE) shown on specific page)
            first_photo = Photo.get_by_id(int(a_first_photo_id))  # get the blogpost with the specific id (a_first_photo_id)

            # check if first_photo exists
            if first_photo:
                # find out the created date of the photo with a_first_photo_id
                created_first_photo = first_photo.created
                
    ##            logging.debug("created_first_photo = " + str(created_first_photo))

                # if 'previous' has been clicked then there are at least ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT photos to show
                # find the younger photos to be shown
                all_photos_plus_one = dataFunctions.find_newer_photos(ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT + 1, created_first_photo)
                
    ##            logging.debug("length of all_photos_plus_one = " + str(len(all_photos_plus_one)))

                # older_link shall appear no matter what
                older_link = "Next &#9658;"

                # decide if newer_link shall be "< previous" or ""
                newer_link = validation.get_previous_link(all_photos_plus_one, ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT)

                # get list of only ROWS_PER_PAGE  * MAX_IMG_ON_ROW_INT or less
                all_photos = dataFunctions.find_newer_photos(ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT, created_first_photo)

                # revers the list
                all_photos.reverse()

            else:   # user has typed some random shit in
                self.redirect('/photos')
                return


##########      AllVideos        #######################

# if there is a_first_video_id, then 'Previous' has been clicked
        if a_first_video_id:
##            logging.debug("Goes into if: 'Previous' has been clicked")

            # find out the video with a_first_video_id (the first video of the 3 (VIDEOS_PER_PAGE) shown on specific page)
            first_video = Video.get_by_id(int(a_first_video_id))  # get the video with the specific id (a_first_video_id)

            # check if first_video exists
            if first_video:
                # find out the created date of the video with a_first_video_id
                created_first_video = first_video.created
                
                # to avoid: BadQueryError: Type Cast Error: unable to cast ['2014-11-11 18:09:25.495000'] with operation DATETIME (unconverted data remains: .495000)            
                #created_last_video = created_last_video[0:19]
                
    ##            logging.debug("created_first_video = " + str(created_first_video))

                # if 'Previous' has been clicked we know that there are at least 3 (VIDEOS_PER_PAGE) videos to show
                # find the previous videos to be shown
                all_videos_plus_one = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(VIDEOS_PER_PAGE+1)
    ##            logging.debug("length of all_videos_plus_one = " + str(len(all_videos_plus_one)))

                # next_link shall appear no matter what
                next_link = "Next &#9658;"

                # decide if previous_link shall be "< Previous" or ""
                previous_link = validation.get_previous_link(all_videos_plus_one, VIDEOS_PER_PAGE)


                all_videos = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(VIDEOS_PER_PAGE)

                # revers the list
                all_videos.reverse()

            else:   # user has typed some random shit in
                self.redirect('/videos')
                return
             
