import httpx
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

csv_path = r'pliki z danymi'
base_url = 'https://www.reddit.com/'

def errory(response):
    if response.status_code == 200:
        return
    elif response.status_code // 100 == 3:
        raise Exception('Error: ' + str(response.status_code) + ', Missing values.')
    elif response.status_code // 100 == 4:
        raise Exception('Error: ' + str(response.status_code) + ', Bad request.')
    elif response.status_code // 100 == 5:
        raise Exception('Error: ' + str(response.status_code) + ', Server error.')
    else:
        raise Exception('Failed to fetch data')

def search_Home_post_id(phrase, category, limit):
    url = base_url + 'search.json?q=' + phrase + '&sort=' + category
    selected_keys_post = ['subreddit', 'selftext', 'title', 'id']
    after_post_id = None
    
    dataset = []

    for x in range(1):
        params = {
            'limit': limit,
            'after': after_post_id
        }
        response = httpx.get(url, params=params)
        errory(response)
        json_data = response.json()
    
        for rec in json_data['data']['children']:
            selected_data_post = {key: rec['data'][key] for key in selected_keys_post}
            dataset.append(selected_data_post)
    
        after_post_id = json_data['data']['after']
    
    return dataset

def search_Post_Comments(name_subreddit, post_id, limit):
    url = base_url + 'r/' + name_subreddit + '/comments/' + post_id + '.json?sort=top'
    selected_keys_comment = ['body']
    dataset = []
    after_comment_id = None

    for x in range(1):
        params = {
            'after': after_comment_id
        }
        response = httpx.get(url, params=params)
        errory(response)
        json_data = response.json()

        comments = json_data[1]['data']['children']
        
        comment_count = 0
    
    for comment in comments:
        if comment_count >= limit:
            break
        comment_data = {key: comment['data'].get(key, None) for key in selected_keys_comment}
        dataset.append(comment_data)
        
        comment_count += 1

        after_comment_id = json_data[1]['data']['after']

    return dataset

def batch_vader(phrases):
    analyzer = SentimentIntensityAnalyzer()
    results = [analyzer.polarity_scores(phrase) for phrase in phrases]
    return results

def batch_bert(phrases):
    classifier = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment")
    max_input_length = classifier.tokenizer.model_max_length
    results = [classifier(phrase[:max_input_length - 2])[0] for phrase in phrases]
    return results

def analyze_posts(posts):
    combined_texts = [post.get('title', '') + " " + post.get('selftext', '') for post in posts]
    vader_results = batch_vader(combined_texts)
    bert_results = batch_bert(combined_texts)

    for post, vader_result, bert_result in zip(posts, vader_results, bert_results):
        post['Post_Opinion'] = {
            'Vader': 'Positive' if vader_result['compound'] >= 0.23 else ('Negative' if vader_result['compound'] <= -0.23 else 'Neutral'),
            'Bert': 'Positive' if bert_result['label'] == "5 stars" else ('Neutral Positive' if bert_result['label'] == "4 stars" else ('Neutral' if bert_result['label'] == "3 stars" else ('Neutral Negative' if bert_result['label'] == "2 stars" else 'Negative')))
        }

    return posts

def analyze_comments(posts):
    for post in posts:
        comments = post.get('comments', [])
        comment_texts = [comment.get('body', '') for comment in comments]

        vader_results = batch_vader(comment_texts)
        bert_results = batch_bert(comment_texts)
        
        for comment, vader_result, bert_result in zip(comments, vader_results, bert_results):
            comment['Comment_Opinion'] = {
                'Vader': 'Positive' if vader_result['compound'] >= 0.23 else ('Negative' if vader_result['compound'] <= -0.23 else 'Neutral'),
                'Bert': 'Positive' if bert_result['label'] == "5 stars" else ('Neutral Positive' if bert_result['label'] == "4 stars" else ('Neutral' if bert_result['label'] == "3 stars" else ('Neutral Negative' if bert_result['label'] == "2 stars" else 'Negative')))
            }
        
    return posts

def link_search_to_profile(phrase, post_limit, comment_limit):
    search_post_id = search_Home_post_id(phrase, 'relevance', post_limit)
    for post in search_post_id:
        subreddit_name = post['subreddit']
        post_id = post['id']
        comments_data = search_Post_Comments(subreddit_name, post_id, comment_limit)
        post['comments'] = comments_data
    
    search_post_id = analyze_posts(search_post_id)
    search_post_id = analyze_comments(search_post_id)
    df = pd.DataFrame(search_post_id)

    csv_path1 = csv_path + '/reddit_posts_and_comments.json'
    df.to_json(csv_path1, index=False)

link_search_to_profile('lego', 23, 9)

import json

csv_path1 = csv_path + '/reddit_posts_and_comments.json'

with open(csv_path1, 'r') as file:
    data = json.load(file)

rows = []

for post_id, comments in data['comments'].items():
    for comment in comments:
        body = comment['body']
        vader_opinion = comment['Comment_Opinion']['Vader']
        bert_opinion = comment['Comment_Opinion']['Bert']
        rows.append({
            'body': body,
            'Vader': vader_opinion,
            'Bert': bert_opinion
        })

df = pd.DataFrame(rows)

csv_path1 = csv_path + '/comments_opinions.csv'
df.to_csv(csv_path1, index=False)