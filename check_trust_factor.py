#check_trust_factor.py

from datetime import datetime
   
def change_date_timestamp(dataset):
    dataset['created_utc'] = dataset['created_utc'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return dataset

def check_Subreddit(df, now):
    if df['subscribers'] is None or df['subscribers'] == 0:
        df['subscribers'] = 1
    
    active_users_percent = df['active_user_count'] / df['subscribers']
    
    trust_factor = round(active_users_percent*1000,3)
    
    created = datetime.utcfromtimestamp(df['created_utc'])
    months = (now.year - created.year) * 12 + now.month - created.month
    
    if df['community_reviewed'] is True:
        trust_factor += 0.2
    
    trust_factor += months / 100
    
    return trust_factor

def check_Profile_info(df, now):
    if (df['created_utc'] is None):
        created = now
    else:
        created = datetime.utcfromtimestamp(df['created_utc'])
    months = (now.year - created.year) * 12 + now.month - created.month
    days = months * 30 + now.day - created.day
    
    if df['is_employee'] is True:
        trust_factor = 0.6
    elif df['verified'] is False:
        trust_factor = 0.0
    elif df['is_gold'] is True:
        trust_factor = 0.6
    else:
        trust_factor = 0.2

    if df['awarder_karma'] > 100:
        trust_factor += 0.25
    elif df['awarder_karma'] > 50:
        trust_factor += 0.2
    elif df['awarder_karma'] > 0:
        trust_factor += 0.1

    if df['total_karma'] > days*100:
        trust_factor += 0.2
    elif df['total_karma'] > days*20:
        trust_factor += 0.15
    elif df['total_karma'] > days:
        trust_factor += 0.1

    if df['awardee_karma'] > days*3:
        trust_factor += 0.2
    elif df['awardee_karma'] > days*2:
        trust_factor += 0.15
    elif df['awardee_karma'] > days:
        trust_factor += 0.1

    trust_factor += months / 100
    
    return trust_factor

def check_Post(df, now, author_trust, subreddit_trust):
    post_created = datetime.utcfromtimestamp(df['created_utc'])
    post_months = (now.year - post_created.year) * 12 + now.month - post_created.month
    post_days = post_months * 30 + now.day - post_created.day
        
    if author_trust >= 0.8:
        trust_factor = 0.3
    elif author_trust >= 0.5:
        trust_factor = 0.25
    elif author_trust >= 0.3:
        trust_factor = 0.2
    else:
        trust_factor = 0.0
    
    if subreddit_trust >= 0.8:
        trust_factor += 0.3
    elif subreddit_trust >= 0.5:
        trust_factor += 0.25
    elif subreddit_trust >= 0.3:
        trust_factor += 0.2
        
    if post_days <= 1:
        trust_factor += 0.2
    elif post_days <= 2:
        trust_factor += 0.15
    elif post_days <= 5:
        trust_factor += 0.1
    
    if df['upvote_ratio'] >= 0.8:
        trust_factor += 0.2
    elif df['upvote_ratio'] > 0.5:
        trust_factor += 0.15
    elif df['upvote_ratio'] >= 3:
        trust_factor += 0.1
        
    return trust_factor

def analyze_trust_factor(data):
    now = datetime.utcnow()
    
    for index, post_info in data['post'].items():
        post = post_info
        subreddit = data['subreddit_info'][index]
        profile = data['profile_info'][index]
        
        subreddit_trust_factor = check_Subreddit(subreddit, now)
        subreddit['trust_factor'] = subreddit_trust_factor
        
        author_trust_factor = check_Profile_info(profile, now)
        profile['trust_factor'] = author_trust_factor
        
        post_trust_factor = check_Post(post, now, author_trust_factor, subreddit_trust_factor)
        data['post'][index]['post_trust_factor'] = post_trust_factor
        
    return data