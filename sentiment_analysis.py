#sentiment_analysis.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def vader(phrases):
    analyzer = SentimentIntensityAnalyzer()
    results = [analyzer.polarity_scores(phrase) for phrase in phrases]
    return results

def analyze_posts(posts):
    combined_texts = [post['title'] + " " + post['selftext'] for post in posts]
    vader_results = vader(combined_texts)

    for post, vader_result in zip(posts, vader_results):
        post['Post_Opinion'] = vader_result['compound']
        
    return posts

def label_vader(compound):
    opinion = 'Positive' if compound >= 0.47 else ('Neutral Positive' if compound > 0.18  else ('Neutral' if compound > -0.26 else ('Neutral Negative' if compound > -0.43 else 'Negative')))
    
    return opinion

def analyze_comments(posts):
    for post_index, comments in posts.get('comments', {}).items():
        comment_texts = [comment.get('body', '') for comment in comments]

        vader_results = vader(comment_texts)
        
        for comment, vader_result in zip(comments, vader_results):
            comment['Comment_Opinion'] = vader_result['compound']
        
    return posts

def count_sentiment(dataframe):
    opinion_sums = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    
    for compound in dataframe:
        if compound >= 0.47:
            opinion_sums['Positive'] += 1
        elif compound > 0.18:
            opinion_sums['Positive'] += 0.5
            opinion_sums['Neutral'] += 0.5
        elif compound >= -0.26:
            opinion_sums['Neutral'] += 1
        elif compound >= -0.43:
            opinion_sums['Negative'] += 0.5
            opinion_sums['Neutral'] += 0.5
        else:
            opinion_sums['Negative'] += 1

    return opinion_sums

def count_upvotes(opinions, upvotes):
    opinion_sums = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    
    for compound, vote_count in zip(opinions, upvotes):
        if vote_count is None or vote_count == 0:
            vote_count = 1
            
        if compound >= 0.47:
            opinion_sums['Positive'] += vote_count
        elif compound > 0.18:
            opinion_sums['Positive'] += vote_count / 2
            opinion_sums['Neutral'] += vote_count / 2
        elif compound >= -0.26:
            opinion_sums['Neutral'] += vote_count
        elif compound >= -0.43:
            opinion_sums['Negative'] += vote_count / 2
            opinion_sums['Neutral'] += vote_count / 2
        else:
            opinion_sums['Negative'] += vote_count

    return opinion_sums