import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

csv_path = r'pliki z danymi'

csv_path1 = csv_path + '/Dane4.csv'
df = pd.read_csv(csv_path1, sep='\t', encoding='latin1')

def batch_vader(phrases):
    analyzer = SentimentIntensityAnalyzer()
    results = [analyzer.polarity_scores(phrase) for phrase in phrases]
    return results

def batch_bert(phrases):
    classifier = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment")
    max_input_length = classifier.tokenizer.model_max_length
    results = [classifier(phrase[:max_input_length - 2])[0] for phrase in phrases]
    return results

def analyze_comments(comments):
    comment_texts = comments['body']

    vader_results = batch_vader(comment_texts)
    bert_results = batch_bert(comment_texts)
    
    vader_sentiments = []
    #bert_sentiments = []
    
    for vader_result, bert_result in zip(vader_results, bert_results):
        #vader_sentiment = vader_result['compound']
        vader_sentiment = 'Positive' if vader_result['compound'] >= 0.47 else ('Neutral Positive' if vader_result['compound'] > 0.18  else ('Neutral' if vader_result['compound'] > -0.26 else ('Neutral Negative' if vader_result['compound'] > -0.43 else 'Negative')))
        vader_sentiments.append(vader_sentiment)
        
        #bert_sentiment = 'Positive' if bert_result['label'] == "5 stars" else ('Neutral Positive' if bert_result['label'] == "4 stars" else ('Neutral' if bert_result['label'] == "3 stars" else ('Neutral Negative' if bert_result['label'] == "2 stars" else 'Negative')))
        #bert_sentiments.append(bert_sentiment)
    
    comments['Vader'] = vader_sentiments
    #comments['Bert'] = bert_sentiments
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
#df['Bert_mapped'] = df['Bert'].map(sentiment_map)

def create_comparison_summary(model):
    summary = {
        'should be positive is positive': len(df[(df[f'{model}_mapped'] == 1) & ((df['Opinion1'] == 1) | (df['Opinion2'] == 1))]),
        'should be positive is neutral': len(df[(df[f'{model}_mapped'] == 1) & ((df['Opinion1'] == 0) | (df['Opinion2'] == 0))]),
        'should be positive is negative': len(df[(df[f'{model}_mapped'] == 1) & ((df['Opinion1'] == -1) | (df['Opinion2'] == -1))]),
        'should be neutral is positive': len(df[(df[f'{model}_mapped'] == 0) & ((df['Opinion1'] == 1) | (df['Opinion2']== 1))]),
        'should be neutral is neutral': len(df[(df[f'{model}_mapped'] == 0) & ((df['Opinion1'] == 0) | (df['Opinion2'] == 0))]),
        'should be neutral is negative': len(df[(df[f'{model}_mapped'] == 0) & ((df['Opinion1'] == -1) | (df['Opinion2'] == -1))]),
        'should be negative is positive': len(df[(df[f'{model}_mapped'] == -1) & ((df['Opinion1'] == 1) | (df['Opinion2'] == 1))]),
        'should be negative is neutral': len(df[(df[f'{model}_mapped'] == -1) & ((df['Opinion1'] == 0) | (df['Opinion2'] == 0))]),
        'should be negative is negative': len(df[(df[f'{model}_mapped'] == -1) & ((df['Opinion1'] == -1) | (df['Opinion2'] == -1))])
    }
    return summary

vader_summary = create_comparison_summary('Vader')
#bert_summary = create_comparison_summary('Bert')

print("Vader Summary:", vader_summary)
#print("Bert Summary:", bert_summary)

import matplotlib.pyplot as plt

df = pd.DataFrame(df)

plt.figure(figsize=(10, 6))

plt.scatter(df['Opinion1'], df['Vader'], color='red', label='Opinion1', alpha=0.6)

plt.scatter(df['Opinion2'], df['Vader'], color='blue', label='Opinion2', alpha=0.6)

plt.legend()

plt.xlabel('Opinions')
plt.ylabel('Vader')

plt.grid(True)

plt.show()

#zakomentowana linijka 31, odkomentowana 32, macierz pomyłek
#zakomentowana 32, odkomnetowana 31, wykres