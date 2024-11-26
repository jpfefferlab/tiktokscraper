import tiktokscraper as tts
import json

### These functions can be executed without using selenium or having a TikTok account

#Collect the metadata of two videos
video_details = tts.get_video_details(["7417415534339280160","7423680782276758817"])
#Show some of the metadata
for video in video_details:
    video=json.loads(video)
    print('Video Description:', video['itemStruct']['desc'])
    print('Profile Name:', video['itemStruct']['author']['uniqueId'])
    print('---')

#Collect the metadata of two profiles
profile_details = tts.get_profile_details(["selenagomez","zachking"])
#Show some of the metadata
for profile in profile_details:
    profile=json.loads(profile)
    print('Username:', profile['user']['uniqueId'])
    print('Profile Description:', profile['user']['signature'])
    print('User Likes:', profile['stats']['heartCount'])
    print('---')

#Collect 100 comments (2*50) for a video
comms = tts.get_comments_from_video("7417415534339280160", 2)
#Show some of the comment information
for comm in comms:
    print('Comment Text:', comm['text'])
    print('Comment Author:', comm['user']['unique_id'])
    print('---')

    
### The following functions can only be executed with a selenium driver

#First use the function start_selenium. This will open a chrome browser.
#Then wait until the TikTok page is loaded and login (see comment in the start_selenium function)
#This will only work when Chrome is installed on your computer
#Alternatively you can also create your own selenium browser
driver = tts.start_selenium() 

#Now you can start: Collect 100 Video Links for a given Keyword
video_links = tts.get_videos_by_keyword('Funny Cats', driver, 30)

#Collect 100 Video Links for a given User
video_links = tts.get_videos_by_user('zachking', driver, 30)
#Show information to the first two video 
video_ids = [v.split('/')[-1] for v in video_links]
video_details = tts.get_video_details(video_ids[0:2])
for video in video_details:
    video=json.loads(video)
    print('Video Description:', video['itemStruct']['desc'])
    print('Profile Name:', video['itemStruct']['author']['uniqueId'])
    print('---')

#Collect 30 followers of a user
follower_links = tts.get_followers_of_user('zachking', driver, 30)  
#Collect 30 followings of a user
following_links = tts.get_followings_of_user('zachking', driver, 30)