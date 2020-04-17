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
import random

# Edit these each time for subreddits, see an example below
# For the sake of avoiding spam, keep this reasonable
subreddits = []

# General subreddits

subreddits.extend(['Sustainable',
              'Futurology',
              'Green',
              'sustainability',
              'ClimateOffensive',
              'ExtinctionRebellion',
              'videos',
              'collapse',
              'nature',
              'climate',
              'GlobalWarming'])


# Sciencey subreddits, choose these carefully
'''
subreddit.extend(['environmental_science',
                    'chemistry',
                    'physics',
                    'geography',
                    'RenewableEnergy'])
'''

# Edit this with a title for the post
title = "How Bhutan's unique political and social landscape has allowed it to become the first modern day carbon negative country in the world."
# Edit this with the relevant media to be shared
url = 'https://youtu.be/0aW-zIkQe9w'

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
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent = '<terminal:botforreddit:1.0 (by /u/OurEdenMedia)>',
                     username = 'OurEdenMedia',
                     password = '')

# Counter for position in subreddits array and errors
pos = 0
errors = 0 

# Function to post in all subreddits
def post(): 
    # Grabs and defines global variables
    global subreddits
    global pos 
    global errors
    global time_delay
    global delay_secs
    global delay_mins
        
    # Try statement for reddit spitting back errors
    # such as: you post too much 
    try:
        # submits to 
        subreddit = reddit.subreddit(subreddits[pos])
        subreddit.submit(title, url=url)
        print('\nPosted to ' + subreddits[pos] + '!')

        # lazy iterator
        pos += 1
        
        # check if posted to all subreddits
        if (pos <= len(subreddits) - 1):
            # Adds a delay of random mins up to 5 + random seconds
            delay_secs = int(random.randint(1,60))
            delay_mins = int(random.randint(1,5))
            print(f"\nWaiting for {delay_mins} minutes and {delay_secs} seconds to post to the next subreddit...")
            time.sleep(delay_mins*60 + delay_secs)
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
                time_delay = int(random.randint(1,60))
                time.sleep(delay_seconds + int(time_delay))
                post()
            # looks for seconds if delay not found for minutes
            else: 
                delay = re.search("(\d+) seconds?", error.message)
                delay_seconds = float(delay.group(1))
                time_delay = int(random.randint(1,60))
                time.sleep(delay_seconds + int(time_delay))
                post()
            
    except: 
        errors += 1 
        if (errors > 5): 
            print('This script has crashed')
            exit(1) 
            
post()
