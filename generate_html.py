#generate_html.py

import os
import html

def generate_distribution_rows(distribution):
    html_table = ""
    for index, row in distribution.iterrows():
        html_table += f'''
        <tr>
            <td><b>Posts Distribution:</b></td><td>{row['Post_ID']}</td><td>{row['Sentiment_Distribution']['Positive']}</td><td>{row['Sentiment_Distribution']['Neutral']}</td><td>{row['Sentiment_Distribution']['Negative']}</td>
        </tr>
        <tr>
            <td><b>Posts Distribution with Score:</b></td><td>{row['Post_ID']}</td><td>{row['Upvotes_Distribution']['Positive']}</td><td>{row['Upvotes_Distribution']['Neutral']}</td><td>{row['Upvotes_Distribution']['Negative']}</td>
        </tr>
        '''
    return html_table

def generate_details_rows(details):
    html_table = ""
    for index, row in details.iterrows():
        html_table += f'''
        <div>
            <table style="margin-left: 2%;"><tr><th>Post {index + 1}:</th></tr></table>
            <table style="width: 95%;">
                <tr><td colspan="9" style="text-align:center;"><b>Details:</b></td></tr>
                <tr><td style="width: 5%;"><b>Post Number:</b></td><td style="width: 20%;"><b>Title:</b></td><td style="width: 40%;"><b>Selftext:</b></td><td style="width: 5%;"><b>Score:</b></td><td style="width: 10%;"><b>Date and Time:</b></td><td style="width: 10%;"><b>Post Sentiment Opinion:</b></td><td style="width: 5%;"><b>Subreddit:</b></td><td><b>Author:</b></td><td style="width: 5%;"><b>Post:</b></td></tr>
                <tr><td>{row['Post_Index']}</td><td>{row['Title']}</td><td>{row['Selftext']}</td><td>{row['Ups']}</td><td>{row['Created']}</td><td>{row['Post_Opinion']}</td><td>{row['Subreddit_Trust_Factor']}</td><td>{row['Author_Trust_Factor']}</td><td>{row['Post_Trust_Factor']}</td></tr>
            </table>
            <table>
                <tr><td colspan="4" style="text-align:center;"><b>Top Comments:</b></td></tr>
                <tr><td><b>Comment Number:</b></td><td><b>Score:</b></td><td><b>Text:</b></td><td><b>Sentiment Opinion:</b></td></tr>
        '''
    
        for i, comment in enumerate(row['Top_Comments'], 1):
            html_table += f'''
            <tr><td>{i}</td><td>{comment['Comment_Score']}</td><td>{comment['Comment_Body']}</td><td>{comment['Comment_Opinion']}</td></tr>
            '''

        html_table += '</table></div>'
    
    return html_table

def generate_section(title, distribution, details):
    html_table = f''' 
    <table style="margin-left: 0%; width: 100%;"><tr><th>{title}:</th></tr></table>
    <div style="width: 90%; display: flex; align-items: center;">
        <table style="width: 35%;"><tr><td colspan="5" style="text-align:center;"><b>Distribution:</b></td></tr>
        <tr><td style="width: 30%;"><b>Label:</b></td><td style="width: 16%;"><b>Post Number:</b></td><td style="width: 18%;"><b>Positive:</b></td><td style="width: 18%;"><b>Neutral:</b></td><td style="width: 18%;"><b>Negative:</b></td></tr>
        {generate_distribution_rows(distribution)}
        </table>
        <div style="text-align: center; margin-left: 1%; margin-bottom: 1%;"><p>{title} Line Chart:</p><iframe src="{title}_Line_Chart.html" style="border: none; height: 500px; width: 1000px;"></iframe>
        </div>
    </div>
    {generate_details_rows(details)}
    '''
    
    return html_table

def generate_html(phrase, folder_name, post_count, positive_distribution, positive_details, neutral_distribution, neutral_details, negative_distribution, negative_details, min_polarity, max_polarity, mean_polarity, date, query_category, query_time, query_safe_mode, formatted_time):
    beg = ""
    mid = ""
    sanitized_phrase = html.escape(phrase)

    beg += f'''
    <tr><td style="width: 60%"></td><td style="width: 30%"><b>Value:</b></td><td><b>Label:</b></td></tr>
    <tr><td><b>Minimal Polarity:</b></td><td>{min_polarity['Value']}</td><td>{min_polarity['Label']}</td></tr>
    <tr><td><b>Maximal Polarity:</b></td><td>{max_polarity['Value']}</td><td>{max_polarity['Label']}</td></tr>
    <tr><td><b>Average Polarity:</b></td><td>{mean_polarity['Value']}</td><td>{mean_polarity['Label']}</td></tr>
    '''
    
    mid += generate_section("Positive", positive_distribution, positive_details)
    mid += generate_section("Neutral", neutral_distribution, neutral_details)
    mid += generate_section("Negative", negative_distribution, negative_details)
    difference = '{difference}'
    
    html_content = f'''<!DOCTYPE html>
    <html lang="pl-PL">
    <head>
        <meta charset="UTF-8">
        <title>Reddit Sentiment Analysis Report</title>
        <link rel="stylesheet" href="../style.css">
        <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>
    </head>
    <body>
        <h1>Sentiment Analysis Report</h1>
        <table style="width: 90%"><tr><td style="width: 10%"><b>Query:</b></td><td>{sanitized_phrase}</td>
        <td style="width: 12%"><b>Fetched and analyzed:</b></td><td style="width: 6%">{formatted_time}</td>
        <td style="width: 10%"><b>Number of Posts:</b></td><td style="width: 6%">{post_count}</td>
        <td style="width: 10%"><b>Generated:</b></td><td style="width: 10%">{date}</td></tr>
        </table>
        <table style="width: 60%"><tr><td style="width: 15%"><b>Query category:</b></td><td style="width: 10%">{query_category}</td>
        <td style="width: 15%"><b>Query time filter:</b></td><td style="width: 10%">{query_time}</td>
        <td style="width: 12%"><b>Safe mode:</b></td><td style="width: 5%">{query_safe_mode}</td>
        <td><b>Time elapsed from data fetch:</b></td><td style="width: 10%" id="output">
        <py-script>
			from datetime import datetime
			from js import document
			date = f'{date}'
			date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
			now = datetime.now()
			difference = (now - date).days
			document.getElementById("output").textContent = f"{difference} days"
        </py-script>
        </td></tr>
        </table>
        <div style="width: 90%; display: flex; align-items: center;"><table class="beg_table">{beg}</table>
        <div style="text-align: center; margin-left: 5%"><p>Sentiment Distribution:</p><iframe src="Sentiment_Distribution.html" style="border: none; height: 350px; width: 450px;"></iframe></div>
        <div style="text-align: center; margin-left: 1%;"><p>Sentiment Distribution with Score:</p><iframe src="Ups_Sentiment_Distribution.html" style="border: none; height: 350px; width: 450px;"></iframe></div></div>
        <div style="border: none;" class="mid_table">{mid}</div>
        <div style="text-align: center; margin-bottom: 2%; border: none;"><p>Word Cloud:</p><img src="Word_Cloud.png" alt="Word Cloud" style="max-width: 75%; border: none;"></div>
        </body>
    </html>
    '''

    html_file_path = os.path.join(folder_name, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)