import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

csv_path = r'pliki z danymi'

csv_path1 = csv_path + '/Dane5.csv'
df = pd.read_csv(csv_path1, sep=',', encoding='latin1')

df['text'] = df['text'].fillna('').astype(str)

def batch_vader(phrases):
    analyzer = SentimentIntensityAnalyzer()
    results = [analyzer.polarity_scores(phrase) for phrase in phrases]
    return results

def analyze_comments(comments):
    comment_texts = comments['text'].fillna('').astype(str)

    vader_results = batch_vader(comment_texts)
    
    vader_sentiments = []
    
    for vader_result in vader_results:
        vader_sentiment = 'Positive' if vader_result['compound'] >= 0.47 else ('Neutral Positive' if vader_result['compound'] > 0.18  else ('Neutral' if vader_result['compound'] > -0.26 else ('Neutral Negative' if vader_result['compound'] > -0.43 else 'Negative')))
        vader_sentiments.append(vader_sentiment)
        
    comments['Vader'] = vader_sentiments
    return comments

df = analyze_comments(df)

sentiment_map = {
    "Positive": 1,
    "Neutral": 0,
    "Negative": -1,
    "Neutral Negative": -0.5,
    "Neutral Positive": 0.5
}

df['Vader_mapped'] = df['Vader'].map(sentiment_map)

def create_comparison_summary(model):
    summary = {
        'should be positive is positive': len(df[(df[f'{model}_mapped'] == 1) & ((df['sentiment'] == 1))]),
        'should be positive is neutral': len(df[(df[f'{model}_mapped'] == 1) & ((df['sentiment'] == 0))]),
        'should be positive is negative': len(df[(df[f'{model}_mapped'] == 1) & ((df['sentiment'] == -1))]),
        'should be neutral is positive': len(df[(df[f'{model}_mapped'] == 0) & ((df['sentiment'] == 1))]),
        'should be neutral is neutral': len(df[(df[f'{model}_mapped'] == 0) & ((df['sentiment'] == 0))]),
        'should be neutral is negative': len(df[(df[f'{model}_mapped'] == 0) & ((df['sentiment'] == -1))]),
        'should be negative is positive': len(df[(df[f'{model}_mapped'] == -1) & ((df['sentiment'] == 1))]),
        'should be negative is neutral': len(df[(df[f'{model}_mapped'] == -1) & ((df['sentiment'] == 0))]),
        'should be negative is negative': len(df[(df[f'{model}_mapped'] == -1) & ((df['sentiment'] == -1))])
    }
    return summary

vader_summary = create_comparison_summary('Vader')

print("Vader Summary:", vader_summary)