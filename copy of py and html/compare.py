# Helper to get list of posts and newer/older links for Post/Video WHEN previous link (newer link) has been clicked!!!
def get_posts_and_links_if_nextlink_clicked(a_post, is_it_photos, find_newer_link, max_posts_per_page):
    """ Takes blogpost, a_post. A boolean is_it_photos and a number max_posts_per_page. A boolean find_newer_link.
        Returns list of all posts and the links strings"""
    
    # find out the created date of the post a_post
    created_post = a_post.created

    if is_it_photos:  # is_it_photos True  (for Photo)
        # find the next photos to be shown
        all_posts_plus_one = dataFunctions.find_older_photos(max_posts_per_page + 1, created_post)

        ##            logging.debug("length of all_posts_plus_one = " + str(len(all_posts_plus_one)))

        # get list of only max_posts_per_page or less
        all_posts = dataFunctions.find_older_photos(max_posts_per_page, created_post)


    else:   # is_it_photos False  (for Video)
        # find the next videos to be shown
        all_posts_plus_one = db.GqlQuery("SELECT * FROM Video WHERE created < :1 ORDER BY created DESC", created_post).fetch(max_posts_per_page+1)
        ##            logging.debug("length of all_posts_plus_one = " + str(len(all_posts_plus_one)))

        # only get list of 3 or less
        all_posts = db.GqlQuery("SELECT * FROM Video WHERE created < :1 ORDER BY created DESC", created_post).fetch(max_posts_per_page)
        

    if find_newer_link:  # find_newer_link True
        # decide if newer_link shall be "< Previous" or ""
        newer_link = validation.get_previous_link(all_posts_plus_one, max_per_page)

        # older_link shall appear no matter what
        older_link = "Next &#9658;"

    else:   # find_newer_link False
        # newer_link shall appear no matter what 
        newer_link = "&#9668; Previous"

        # decide if older_link shall be "Next >" or ""  
        older_link = validation.get_next_link(all_posts_plus_one, max_per_page)

    return all_posts, newer_link, older_link




##########      AllPhotos        #######################
# find out the created date of the photo with a_last_photo_id
created_last_photo = last_photo.created

##            logging.debug("created_last_photo = " + str(created_last_photo))

# find the next photos to be shown
all_photos_plus_one = dataFunctions.find_older_photos(ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT + 1, created_last_photo)

##            logging.debug("length of all_photos_plus_one = " + str(len(all_photos_plus_one)))

# get list of only ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT or less
all_photos = dataFunctions.find_older_photos(ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT, created_last_photo)




# newer_link shall appear no matter what
newer_link = "&#9668; Previous"

# decide if older_link shall be "Next >" or ""
older_link = validation.get_next_link(all_photos_plus_one, ROWS_PER_PAGE * MAX_IMG_ON_ROW_INT)

         



##########      AllVideos        #######################
# find out the created date of the video with a_last_video_id
created_last_video = last_video.created

##            logging.debug("created_last_video = " + str(created_last_video))

# find the next videos to be shown
all_videos_plus_one = db.GqlQuery("SELECT * FROM Video WHERE created < :1 ORDER BY created DESC", created_last_video).fetch(VIDEOS_PER_PAGE+1)
##            logging.debug("length of all_videos_plus_one = " + str(len(all_videos_plus_one)))

# only get list of 3 or less
all_videos = db.GqlQuery("SELECT * FROM Video WHERE created < :1 ORDER BY created DESC", created_last_video).fetch(VIDEOS_PER_PAGE)



# previous_link shall appear no matter what
previous_link = "&#9668; Previous"

# decide if next_link shall be "Next >" or ""
next_link = validation.get_next_link(all_videos_plus_one, VIDEOS_PER_PAGE)



             
