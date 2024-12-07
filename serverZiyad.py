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

    file_name = f"{name}_{requested_type}_{GROUP_ID}.json"
    with open(file_name, 'w') as json_file:
        json.dump(news_info, json_file, indent=5)

    # Process and send the response based on the requested type
    if requested_type == "headlines":
        articles = p_headlines(news_info)
        response_data = {'type': 'headlines', 'data': articles[:15]}  
        socket.send(json.dumps(response_data).encode())
    elif requested_type == "sources":
        sources = p_sources(news_info)
        response_data = {'type': 'sources', 'data': sources[:15]}  

def result_handler(socket, name):
    while True:
        requested_data = socket.recv(1024).decode()  
        if requested_data.lower() == "exit":  # Check if client wants to terminate
            print(f"Client {name}  terminated from the session.")
            socket.close()
            break

        request = json.loads(requested_data) 
        query = request.get('query') 
        requested_type = request.get('type') 

        print(f"Received a request from {name} with the query '{query}' and type '{requested_type}'.")
        p_request(socket, query, requested_type, name)  

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSock:
            serverSock.bind((HOST, PORT)) 
            serverSock.listen(3)  
            print(f"Server is up and running on port: {PORT}")

            while True:
                try:
                    client_socket, client_addr = serverSock.accept() 
                    print(f"Connection established with {client_addr}")

                    client_thread = threading.Thread(target=result_handler, args=(client_socket, client_addr))
                    client_thread.start()
                except Exception as e:
                    print(f"Error accepting connection: {e}")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    main() 
