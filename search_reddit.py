#search_reddit.py

import httpx
import PySimpleGUI as sg

base_url = 'https://www.reddit.com/'

def errory(response):
    if response.status_code == 200:
        return
    elif response.status_code // 100 == 3:
        raise Exception('Error: ' + str(response.status_code) + ', Missing values.')
        sg.popup_error('Error: ' + str(response.status_code) + ', Missing values.')
    elif response.status_code // 100 == 4:
        raise Exception('Error: ' + str(response.status_code) + ', Bad request.')
        sg.popup_error('Error: ' + str(response.status_code) + ', Bad request.')
    elif response.status_code // 100 == 5:
        raise Exception('Error: ' + str(response.status_code) + ', Server error.')
        sg.popup_error('Error: ' + str(response.status_code) + ', Server error.')
    else:
        raise Exception('Failed to fetch data')
        sg.popup_error('Failed to fetch data')

def search_Home_post_id(phrase, category, limit, time, safe_mode):
    safe_mode = '1' if safe_mode == 'off' else '0'
    category = 'comments' if category == 'most comments' else category
    time = '' if time == 'all time' else f'&t={time}'

    url = base_url + 'search.json?q=' + phrase + '&sort=' + category + '&nsfw=' + safe_mode + time
    selected_keys_post = ['selftext', 'title', 'ups', 'id', 'num_comments', 'created_utc', 'subreddit']
    
    dataset = []
    total_fetched = 0

    while total_fetched < limit:
        remaining = limit - total_fetched
        params = {
            'limit': min(100, remaining)
        }
        response = httpx.get(url, params=params)
        errory(response)
        json_data = response.json()
    
        for rec in json_data['data']['children']:
            selected_data_post = {key: rec['data'][key] for key in selected_keys_post}
            dataset.append(selected_data_post)
        
        total_fetched += len(json_data['data']['children'])
        
    return dataset, total_fetched

def search_Post_Comments(name_subreddit, post_id, limit):
    url = base_url + 'r/' + name_subreddit + '/comments/' + post_id + '.json?sort=top'
    selected_keys_post = ['upvote_ratio', 'author', 'created_utc']
    selected_keys_comment = ['author', 'created_utc', 'score', 'body', 'stickied']
    
    dataset = {
        "post": {},
        "comments": []
    }
    
    after_comment_id = None
    comment_count = 0

    while comment_count < limit:
        params = {
            'after': after_comment_id
        }

        response = httpx.get(url, params=params)
        errory(response)
        json_data = response.json()

        if comment_count == 0:
            post_data = json_data[0]['data']['children'][0]['data']
            dataset['post'] = {key: post_data.get(key, None) for key in selected_keys_post}

        comments = json_data[1]['data']['children']
        if not comments:
            break
        
        for comment in comments:
            comment_data = comment['data']

            if comment_data.get('stickied', False) and comment_count == 0:
                continue
            
            body = comment_data.get('body')
            if body == '[removed]' or body == '[deleted]' or body == '':
                continue
            
            filtered_comment = {key: comment_data.get(key, None) for key in selected_keys_comment}
            dataset['comments'].append(filtered_comment)

            comment_count += 1
            if comment_count >= limit:
                break

        after_comment_id = json_data[1]['data'].get('after')
        
        if after_comment_id is None:
            break
        
    return dataset

def searchProfile_info(name_profile):
    url = base_url + 'user/' + name_profile + '/about.json'
    selected_keys = ['is_employee', 'awardee_karma', 'verified', 'is_gold', 'awarder_karma', 'total_karma', 'name', 'created_utc']

    response = httpx.get(url)
    errory(response)
    json_data = response.json()
    
    user_data = json_data['data']
    
    filtered_data_set = {key: user_data.get(key, None) for key in selected_keys}

    return filtered_data_set

def searchSubreddit_info(name_subreddit):
    url = base_url + 'r/' + name_subreddit + '/about.json'
    selected_keys = ['display_name', 'active_user_count', 'subscribers', 'community_reviewed', 'created_utc']

    response = httpx.get(url)
    errory(response) 
    json_data = response.json()
        
    subreddit_data = json_data['data']
    
    filtered_data_set = {key: subreddit_data.get(key, None) for key in selected_keys}
    
    return filtered_data_set