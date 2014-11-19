


##########      AllBlogPosts        #######################




##########      FullYearBlogPosts        #######################




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
             
