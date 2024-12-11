import socket
import json
import requests
import threading
import extractors
from config import API_KEY, HOST, PORT, GROUP_ID,Maximum_threads 



threadingSemaphor = threading.Semaphore(Maximum_threads)
def handler(clientSoc,clientName):
 with threadingSemaphor:

    while True:
        # Use the socket object `clientSoc` to receive data
        requestInformation = clientSoc.recv(1024).decode()

        # Process the request
        request = json.loads(requestInformation)
        
        Userquery = request.get('query')
        
        data_type = request.get('type') 

        if requestInformation == "exit":  # Check for termination signal
            print(f"Client {clientName} left.")
            clientSoc.close()  # Close the socket properly
            break
        
        print(f"Processing request: query='{Userquery}', type='{data_type}'")
           
        
        api_url = f'https://newsapi.org/v2/{Userquery}&apiKey={API_KEY}'  # here we Construct an API URL
        response = requests.get(api_url)

        if response.status_code != 200:
            print(f"Error occured: with status code {response.status_code}")
            return 

        news_data = response.json()  
        file_name = f"{clientName}_{data_type}_{GROUP_ID}.json" 