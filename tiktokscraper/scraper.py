import requests
import re
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
chromedriver_autoinstaller.install() 

def get_video_details(video_ids):
    """ 
        Get the metadata of one or more videos. This metadata includes for example the video title and description. 
        More information on how a video metadata object looks like can be found in the chapter source.

        :param List[str] videos: Provide video id(s) in a list of strings, eg. ["7417415534339280160","7423680782276758817"]. The id of a video can be found in the link to this video. 
        :returns: A list of video metadata objects (see source)
        :rtype: list

    """
    
    video_details = []
    for video_id in video_ids:
        url=f"https://m.tiktok.com/v/{video_id}.html"
        response = requests.get(url)

        if response.status_code == 200:
            # Check if the target marker is in the HTML
            if '__UNIVERSAL_DATA_FOR_REHYDRATION__' in response.text:
                # Define the regex pattern to extract the data
                item_info = re.compile(r'webapp\.video-detail":{"itemInfo":(.*?),"shareMeta"')

                # Search for matches in the HTML response
                result = re.findall(item_info, response.text)

                # Print or process the result
                if result:
                    video_details.append(result[0])
                else:
                    print(f"Error: No data found for {video_id}")
            else:
                print(f"Error: No data found for {video_id}")
        else:
            print(f"Failed to retrieve data for {video_id}. Status code: {response.status_code}")
            
    return(video_details)



def get_profile_details(profile_names):
    """ Return profile metadata for a given user. This metadata includes for example the users statistics and privacy settings. 
        More information on how a profile metadata object looks like can be found in the chapter source.

        :param List[str] profilenames: Provide usernames in a list of strings, eg. ["selenagomez", "zachking"]. The name of a user can be found in the link to the users profile, (e.g. https://www.tiktok.com/@selenagomez). 
        :returns: A list of profile metadata objects (see source)
        :rtype: list
    """
    
    profile_details =[]
    
    for profile_name in profile_names:
        url=f"https://www.tiktok.com/@{profile_name}"
        response = requests.get(url)

        if '__UNIVERSAL_DATA_FOR_REHYDRATION__' in response.text:
            # Define the regex pattern to extract the data
            item_info = re.compile(r'webapp\.user-detail":{"userInfo":(.*?),"shareMeta"')

            # Search for matches in the HTML response
            result = re.findall(item_info, response.text)

            # Print or process the result
            if result:
                profile_details.append(result[0])
            else:
                print(f"Error: No data found for {profile_name}")
        else:
            print(f"Error: No data found for {profile_name}")
            
    return(profile_details)



def get_comments_from_video(video_id, calls):
    """
        Return the comments metadata for a given video. This metadata includes for example the comments text and language. 
        More information on how a comment metadata object looks like can be found in the chapter source.
        Caution: The comment count of a user includes the number of original comments as well as the number of comment replies (comments to comments).
        With this function, you can only collect original comments, thus the number of collected comments will be less than the comment count.

        :param str video_id: Provide a video id as strings, eg. "7417415534339280160". The id of a video can be found in the link to this video. 
        :param int calls: The number of calls for the function. Each call will return approximately 50 comments (as long as there are still comments to collect).        
        :returns: A list of comment metadata objects (see source)
        :rtype: list
    """
    cursor = 0
    calls = calls*50
    comments = []

    while cursor<calls:
        url =f"https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={video_id}&count=9999999&cursor={cursor}"
        response = requests.get(url).json()
        if response["comments"]!=[]:
            comments += response["comments"]
        else:
            #no more comments
            break
        cursor += 50
    return comments



def start_selenium():
    """ This function will start an automated browser and first open wikipedia, then TikTok. 
        Wait until the TikTok page is fully loaded. Then, you can manually login to TikTok,
        and answer the questions you are asked by TikTok (e.g. solve a captcha or disable cookies
        when asked). Once you are finished and the Tiktok Newsfeed is fully visible, you can
        execute the next function, using this driver object.
        
        Alternatively, if you want to use another browser, you can use your own function to create a driver object.
        
        Caution: With this function, we try to simulate a normal Chrome browser, not a test browser (as TikTok
        sometimes prevents the login from test browsers). To make this work, the Chrome browser needs to be installed
        on your system. If this functions starts a browser in a test environment, check whether you have chrome installed.
        
        :returns: A driver object. This can be inserted in each function requiring the driver.
    """
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--profile-directory=Default")
    options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})
    driver = webdriver.Chrome(options=options)
    
    #Open Wikipedia, so that we have another start adress
    driver.get("https://en.wikipedia.org")
    time.sleep(random.randint(2,4))
    
    #Open Tiktok
    driver.get("https://www.tiktok.com")
    return(driver)


def get_videos_by_keyword(keyword, driver, limit):
    """
        Perform a keyword-search and collect the ids of the videos of the search results. 
        
        Caution: The TikTok keyword search will show anything related to a keyword. If you search for the 
        word "dog", it will give you videos with dog in the title, the music title, the username and more.
        
        Requires the execution of start_selenium and login to TikTok first.

        :param str keyword: You can either use a keyword (e.g. "dog" or "funny dog") or a hashtag (e.g. "#dog") 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int limit: Limit the number of results. If the number of search results exceeds this value, the function will return the ids of the top l videos (or a little bit more).
        :returns: List of video links, e.g. ["https://www.tiktok.com/@alvathehotdog/ video/7389719882289483041", "https://www.tiktok.com/@unilad/ video/7010775526902107398"]
        :rtype: list
    """
        
    # Navigate to TikTok search page
    url = f"https://www.tiktok.com/search?q={keyword}"
    driver.get(url)
    time.sleep(random.randint(4,8))  # Wait for the page to load

    video_links=set()
    
    while len(video_links)<limit:  
        # Scroll down to load more videos
        scroll_duration=random.randint(3,7)
        end_time = time.time() + scroll_duration
        while time.time() < end_time:
            driver.find_element("xpath", "//body").send_keys(Keys.ARROW_DOWN)
        
        #Extract videos
        time.sleep(random.randint(1,2))
        elements=driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
        for el in elements:
            try:
                video_links.add(el.get_attribute("href"))
            except:
                continue
        video_links = list(set(video_links))  # Remove duplicates
        
        #Check, whether end of page reached
        current_scroll_position = driver.execute_script("return window.scrollY")
        total_page_height = driver.execute_script("return document.body.scrollHeight")
        visible_window_height = driver.execute_script("return window.innerHeight")
        if current_scroll_position + visible_window_height >= total_page_height:
            break

    return list(video_links)


def get_videos_by_user(profile_name, driver, limit):
    """
        Collect the ids of the videos for a given profile. 
        Requires the execution of start_selenium and login to TikTok first.

        :param str profile_name: Provide one username, eg. "selenagomez". The name of a user can be found in the link to the users profile, (e.g. https://www.tiktok.com/@selenagomez). 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int limit: Limit the number of results. If the number of user videos exceeds this value, the function will return the ids of the top l videos (or a little bit more).
        :returns: List of video links, e.g. ["https://www.tiktok.com/@alvathehotdog/ video/7389719882289483041", "https://www.tiktok.com/@unilad/ video/7010775526902107398"]
        :rtype: list
    """

    #Open profile
    url = f"https://www.tiktok.com/@{profile_name}"
    driver.get(url)
    time.sleep(random.randint(4,8))  # Wait for the page to load

    video_links=set()
    
    while len(video_links)<limit:  
        # Scroll down to load more videos
        scroll_duration=random.randint(1,2)
        end_time = time.time() + scroll_duration
        while time.time() < end_time:
            driver.find_element("xpath", "//body").send_keys(Keys.ARROW_DOWN)
            
        #Extract videos
        time.sleep(random.randint(1,2))
        elements=driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
        for el in elements:
            try:
                video_links.add(el.get_attribute("href"))
            except:
                continue
        
        #Check, whether end of page reached
        current_scroll_position = driver.execute_script("return window.scrollY")
        total_page_height = driver.execute_script("return document.body.scrollHeight")
        visible_window_height = driver.execute_script("return window.innerHeight")
        if current_scroll_position + visible_window_height >= total_page_height:
            break
            
        #Pause a little
        time.sleep(random.randint(2,5))

    return list(video_links)


def get_followers_of_user(profile_name, driver, limit):
    """
        Return the followers for a given user. 
        Requires the execution of start_selenium and login to TikTok first.
        Caution: Sometimes, the follower count displayed on TikTok is higher than the actual number of followers shown on TikTok.

        :param str profile_name: Provide one username, eg. "selenagomez". The name of a user can be found in the link to the users profile, (e.g. https://www.tiktok.com/@selenagomez). 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int limit: Limit the number of results. If the number of followers exceeds this value, the function will return the names of the top l followers (or a little bit more).
        :returns: A list of follower links, eg. ["https://www.tiktok.com/@imranadil915", "https://www.tiktok.com/@user161624720276"].
        :rtype: list
    """

    #Open profile page
    url = f"https://www.tiktok.com/@{profile_name}"
    driver.get(url)
    time.sleep(random.randint(4,6))  

    #Click on follower tab
    followers_button = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='followers']")
    followers_button.click()
    followers_container = driver.find_element(By.CSS_SELECTOR, "div.css-wq5jjc-DivUserListContainer.eorzdsw0")
    time.sleep(random.randint(4,6))  
    
    followers=set()    
    while len(followers)<limit:  
        #Extract followers
        link_elements = driver.find_elements(By.CSS_SELECTOR, "a.es616eb3.css-5c23qb-StyledLink-StyledUserInfoLink.er1vbsz0")
        current_followers = set([link.get_attribute("href") for link in link_elements])
        new_followers = current_followers.difference(followers)
        
        #Check, whether end of page reached
        if new_followers==set():
            break
        
        #Add new followers
        followers = followers.union(new_followers)
        
        # Scroll down to load more followers
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", followers_container)
        time.sleep(random.randint(4,6)) 

    return list(followers)


def get_followings_of_user(profile_name, driver, limit):
    """
        Return the links to users following a given profile. 
        Requires the execution of start_selenium and login to TikTok first.
        Caution: Sometimes, the following count displayed on TikTok is higher than the actual number of followers shown on TikTok.
        Caution: The list of followings is private for many users, thus collecting the followings might not reveal any results.
        
        :param str profile_name: Provide one username, eg. "selenagomez". The name of a user can be found in the link to the users profile, (e.g. https://www.tiktok.com/@selenagomez). 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int limit: Limit the number of results. If the number of followings exceeds this value, the function will return the names of the top l followings (or a little bit more).
        :returns: A list of following links, eg. ["https://www.tiktok.com/@imranadil915", "https://www.tiktok.com/@user161624720276"].
        :rtype: list
    """
    
    #go_to_profile_page
    url = f"https://www.tiktok.com/@{profile_name}"
    driver.get(url)
    time.sleep(random.randint(3,5))  # Wait for the page to load

    #Click on following tab
    following_button = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='following']")
    following_button.click()
    followings_container = driver.find_element(By.CSS_SELECTOR, "div.css-wq5jjc-DivUserListContainer.eorzdsw0")
    time.sleep(random.randint(3,5))    
    
    followings=set()
    while len(followings)<limit: 
        #Extract followings
        link_elements = driver.find_elements(By.CSS_SELECTOR, "a.es616eb3.css-5c23qb-StyledLink-StyledUserInfoLink.er1vbsz0")
        current_followings = set([link.get_attribute("href") for link in link_elements])
        new_followings = current_followings.difference(followings)
        
        #Check, whether end of page reached
        if new_followings==set():
            break
        
        #Add new followings
        followings = followings.union(new_followings)
        
        # Scroll down to load more followers
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", followings_container)
        time.sleep(random.randint(3,4)) 

    return list(followings)