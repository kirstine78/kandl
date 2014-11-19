# Helper to get list of photos/videos and newer older/links for Photo/Video WHEN previous link (newer link) has been clicked!!!
def get_blog_posts_and_links_if_prevlink_clicked(an_id, a_post, is_it_photos, find_previous_link, max_per_page):
    """ Takes an_id and post, a_post. A boolean is_it_photos and a number max_per_page. A boolean find_previous_link.
        Returns list of all blog posts and the links strings"""  

    if is_it_photos:  # is_it_photos True  (for Photo)
        # find out the created date of the photo with a_first_photo_id
        created_first_photo = a_post.created

        # if 'previous' has been clicked then there are at least ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT photos to show
        # find the younger photos to be shown
        all_posts_plus_one = find_newer_photos(max_per_page + 1, created_first_photo)

        ##            logging.debug("length of all_photos_plus_one = " + str(len(all_photos_plus_one)))
        # get list of only ROWS_PER_PAGE  * MAX_IMG_ON_ROW_INT or less
        all_photos = dataFunctions.find_newer_photos(max_per_page, created_first_photo)

        
    else:   # is_it_photos False  (for Video)
        
        # find out the created date of the post with an_id
        created_first_video = a_post.created

        # if 'newer posts' has been clicked we know that there are at least max_posts_per_page posts to show
        # find the posts to be shown
        all_posts_plus_one = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(max_per_page+1)
##            logging.debug("length of all_posts_plus_one = " + str(len(all_posts_plus_one)))

        # get list of only max_posts_per_page or less
        all_posts = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(max_per_page)




##        # find out the created date of the video with a_first_video_id
##        created_first_video = first_video.created
##
##        ##            logging.debug("created_first_video = " + str(created_first_video))
##
##        # if 'Previous' has been clicked we know that there are at least 3 (VIDEOS_PER_PAGE) videos to show
##        # find the previous videos to be shown
##        all_videos_plus_one = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(VIDEOS_PER_PAGE+1)
##        ##            logging.debug("length of all_videos_plus_one = " + str(len(all_videos_plus_one)))
##        all_videos = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(VIDEOS_PER_PAGE)


    # reverse, cause you get ASC and you want DESC
    all_posts.reverse()

    if find_previous_link:  # find_previous_link True
        # decide if newer_link shall be "< Previous" or ""
        newer_link = validation.get_previous_link(all_posts_plus_one, max_posts_per_page)

        # older_link shall appear no matter what
        older_link = "Next &#9658;"

    else:   # find_previous_link False
        # newer_link shall appear no matter what 
        newer_link = "&#9668; Previous"

        # decide if older_link shall be "Next >" or ""  
        older_link = validation.get_next_link(all_posts_plus_one, max_posts_per_page)

    return all_posts, newer_link, older_link




##########      AllPhotos        #######################
            
# if there is a_first_photo_id, then 'previous' has been clicked

# find out the created date of the photo with a_first_photo_id
created_first_photo = first_photo.created

##            logging.debug("created_first_photo = " + str(created_first_photo))

# if 'previous' has been clicked then there are at least ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT photos to show
# find the younger photos to be shown
all_photos_plus_one = dataFunctions.find_newer_photos(ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT + 1, created_first_photo)

##            logging.debug("length of all_photos_plus_one = " + str(len(all_photos_plus_one)))
# get list of only ROWS_PER_PAGE  * MAX_IMG_ON_ROW_INT or less
all_photos = dataFunctions.find_newer_photos(ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT, created_first_photo)



# older_link shall appear no matter what
older_link = "Next &#9658;"

# decide if newer_link shall be "< previous" or ""
newer_link = validation.get_previous_link(all_photos_plus_one, ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT)



# revers the list
all_photos.reverse()


##########      AllVideos        #######################

# if there is a_first_video_id, then 'Previous' has been clicked

# find out the created date of the video with a_first_video_id
created_first_video = first_video.created

##            logging.debug("created_first_video = " + str(created_first_video))

# if 'Previous' has been clicked we know that there are at least 3 (VIDEOS_PER_PAGE) videos to show
# find the previous videos to be shown
all_videos_plus_one = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(VIDEOS_PER_PAGE+1)
##            logging.debug("length of all_videos_plus_one = " + str(len(all_videos_plus_one)))
all_videos = db.GqlQuery("SELECT * FROM Video WHERE created > :1 ORDER BY created ASC", created_first_video).fetch(VIDEOS_PER_PAGE)

# next_link shall appear no matter what
next_link = "Next &#9658;"

# decide if previous_link shall be "< Previous" or ""
previous_link = validation.get_previous_link(all_videos_plus_one, VIDEOS_PER_PAGE)




# revers the list
all_videos.reverse()
             
