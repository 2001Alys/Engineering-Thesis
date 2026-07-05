from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline
import pandas as pd
import time

def nltk(phrases):
    start_time = time.time()
    results = []
    sid = SentimentIntensityAnalyzer()

    for phrase in phrases:
        sentiment_score = sid.polarity_scores(phrase)
        if sentiment_score['compound'] >= 0.05:
            sentiment = "Positive"
        elif sentiment_score['compound'] <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        results.append(sentiment)
        
    execution_time = time.time() - start_time
    return results, execution_time

def vader(phrases):
    start_time = time.time()
    results = []
    analyzer = SentimentIntensityAnalyzer()

    for phrase in phrases:
        sentiment = analyzer.polarity_scores(phrase)
        if sentiment['compound'] >= 0.05:
            sentiment_label = "Positive"
        elif sentiment['compound'] <= -0.05:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"
        results.append(sentiment_label)
        
    execution_time = time.time() - start_time
    return results, execution_time

def textblob(phrases):
    start_time = time.time()
    results = []
    for phrase in phrases:
        blob = TextBlob(phrase)
        sentiment = blob.sentiment
        if sentiment.polarity > 0:
            sentiment_label = "Positive"
        elif sentiment.polarity < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"
        results.append(sentiment_label)
        
    execution_time = time.time() - start_time
    return results, execution_time

def bert(phrases):
    start_time = time.time()
    results = []
    classifier = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment")
    
    for phrase in phrases:
        sentiment = classifier(phrase)[0]
        sentiment_label = sentiment['label']
        if sentiment_label == "1 star":
            sentiment_label = "Negative"
        elif sentiment_label == "3 stars" or sentiment_label == "2 stars" or sentiment_label == "4 stars":
            sentiment_label = "Neutral"
        else:
            sentiment_label = "Positive"
        results.append(sentiment_label)
        
    execution_time = time.time() - start_time
    return results, execution_time

def roberta(phrases):
    start_time = time.time()
    results = []
    classifier = pipeline('sentiment-analysis', model="cardiffnlp/twitter-roberta-base-sentiment")
    
    for phrase in phrases:
        sentiment = classifier(phrase)[0]
        sentiment_label = sentiment['label']
        if sentiment_label == "negative":
            sentiment_label = "Negative"
        elif sentiment_label == "neutral":
            sentiment_label = "Neutral"
        else:
            sentiment_label = "Positive"
        results.append(sentiment_label)
        
    execution_time = time.time() - start_time
    return results, execution_time

def distilbert(phrases):
    start_time = time.time()
    results = []
    classifier = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")
    
    for phrase in phrases:
        sentiment = classifier(phrase)[0]
        sentiment_label = sentiment['label']
        if sentiment_label == "NEGATIVE":
            sentiment_label = "Negative"
        elif sentiment_label == "POSITIVE":
            sentiment_label = "Positive"
        else:
            sentiment_label = "Neutral"
        results.append(sentiment_label)
        
    execution_time = time.time() - start_time
    return results, execution_time

def prof_comments():
    csv_path = r'pliki z danymi'
    df = pd.read_csv(csv_path + '\Dane3.csv')
    phrases = df['body'].fillna('') + ' ' + df['selftext'].fillna('')
    
    nltk_results, nltk_time = nltk(phrases)
    vader_results, vader_time = vader(phrases)
    textblob_results, textblob_time = textblob(phrases)
    bert_results, bert_time = bert(phrases)
    roberta_results, roberta_time = roberta(phrases)
    distilbert_results, distilbert_time = distilbert(phrases)
    
    results_df = pd.DataFrame({
        'Body': df['body'],
        'Selftext': df['selftext'],
        'NLTK': nltk_results,
        'Vader': vader_results,
        'TextBlob': textblob_results,
        'BERT': bert_results,
        'RoBERTa': roberta_results,
        'DistilBERT': distilbert_results
    })
    
    results_file = r'pliki z danymi\Dane2.csv'
    
    results_df.to_csv(results_file, index=False, encoding='utf-8')
    
    print("NLTK Time:", nltk_time)
    print("VADER Time:", vader_time)
    print("TextBlob Time:", textblob_time)
    print("BERT Time:", bert_time)
    print("RoBERTa Time:", roberta_time)
    print("DistilBERT Time:", distilbert_time)

prof_comments()