def extract_headlines(news_data):

    return [
        {
            'source_name': article.get('source', {}).get('name'),
            'author': article.get('author'),
            'title': article.get('title'),
            'url': article.get('url'),
            'description': article.get('description'),
            'publish_date': article.get('publishedAt', '')[:10],  
            'publish_time': article.get('publishedAt', '')[11:19], 
        }
        for article in news_data.get('articles', [])
    ]