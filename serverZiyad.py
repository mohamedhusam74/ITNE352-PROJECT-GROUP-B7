import socket  
import json  
import requests  
import threading  

# Server configuration
HOST = '127.0.0.1' 
PORT = 34142  
API_KEY = "ea46e59a1e754401b72c3cb895e374e7"  
GROUP_ID = "B7"  


#Processing headlines
def p_headlines(news_info):
    """
    Parse and extract headlines from the NewsAPI response.
    :param news_info: Dictionary containing news articles
    :return: List of dictionaries with parsed article details
    """
    articles = []
    for article in news_info.get('articles', []):
        articles.append({
            'source_name': article.get('source', {}).get('name'),
            'author': article.get('author'),
            'title': article.get('title'),
            'url': article.get('url'),
            'description': article.get('description'),
            'publish_date': article.get('publishedAt', '')[:10],  
            'publish_time': article.get('publishedAt', '')[11:19],  
        })
    return articles

#Processing sources
def p_sources(news_info):
    sources = []
    for source in news_info.get('sources', []):
        sources.append({
            'source_name': source.get('name'),
            'country': source.get('country'),
            'description': source.get('description'),
            'url': source.get('url'),
            'category': source.get('category'),
            'language': source.get('language'),
        })
    return sources

def p_request(socket, query, requested_type, name):
    api = f'https://newsapi.org/v2/{query}&apiKey={API_KEY}'  # Construct API URL
    result = requests.get(api)  


    if result.status_code == 200:  
        news_info = result.json()  
    else:
        print(f"Status Code: {result.status_code} has encountered error")
        return


