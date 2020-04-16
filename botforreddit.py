# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:39:16 2020

@author: Cam
Edited from https://www.youtube.com/watch?v=ujflrixMl8I
"""

# You may have to install these:
# Type 'pip install praw' etc to do so
import praw 
import re
import time 
import numpy as np

# Edit these each time for subreddits, see an example below
# For the sake of avoiding spam, keep this reasonable
subreddits = ['sustainability', 
              'ExtinctionRebellion', 
              'environmental_science',
              'Green',
              'FridaysForFuture',
              'Sustainable',
              'Futurology']
# Edit this with a title for the post
title = 'The science behind a group of chemicals called PFASs, the chemicals at the focal point of the film Dark Waters, which discusses how the chemicals contaminated drinking water across America'
# Edit this with the relevant media to be shared
url = 'https://www.youtube.com/watch?v=UGa-MWSuVdk'

# API connection to reddit
#
# Note: If you want to set this up for another account:
# 1. Go to https://www.reddit.com/prefs/apps
# 2. Create an script app
#    I used: about = https://localhost.com/about
#    Redirect = https://newsitesss.com/redirect
# 3. Edit 'client_id' in code below to the code
#    underneath personal use script, undereneath the app name
# 4. Edit 'client_secret' in code below to secret on web page
# 5. Edit the username and password
reddit = praw.Reddit(client_id='ILsFGH8r7R6L5A',
                     client_secret='yyMhiynw9rCqp1i4ykR2aSTrCD8',
                     user_agent = '<terminal:botforreddit:1.0 (by /u/OurEdenMedia)>',
                     username = 'OurEdenMedia',
                     password = '')

# Counter for position in subreddits array and errors
pos = 0
errors = 0 

# Function to post in all subreddits
def post(): 
    # Grabs global variables
    global subreddits
    global pos 
    global errors
    
    # Try statement for reddit spitting back errors
    # such as: you post too much 
    try:
        # submits to 
        subreddit = reddit.subreddit(subreddits[pos])
        subreddit.submit(title, url=url)

        # lazy iterator
        pos += 1
        
        # check if posted to all subreddits
        if pos <= len(subreddits) - 1:
            # calls post function again after a time delay
            time_delay = np.randint(low=1, high=5)
            time_delay2 = np.randint(low=1, high=60)
            time.sleep(5 + int(time_delay)*60 + time_delay2)
            post()
        else:
            print('Done!')
    
    # Error testing
    except praw.exceptions.APIException as error:
        if (error.error_type == 'RATELIMIT'):
            # searches for d minutes
            delay = re.search("(\d+) minutes?", error.message)
            
            if delay: 
                delay_seconds = float(int(delay.group(1)) * 60)
                time_delay = np.randint(low=1, high=60)
                time.sleep(delay_seconds + int(time_delay))
                post()
            # looks for seconds if delay not found for minutes
            else: 
                delay = re.search("(\d+) seconds?", error.message)
                delay_seconds = float(delay.group(1))
                time_delay = np.randint(low=1, high=60)
                time.sleep(delay_seconds + int(time_delay))
                post()
            
    except: 
        errors += 1 
        if (errors > 5): 
            print('This script has crashed')
            exit(1) 
            
post()