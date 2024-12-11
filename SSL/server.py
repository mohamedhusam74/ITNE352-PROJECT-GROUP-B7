import socket
import json
import requests
import threading
import ssl
from config import API_KEY, HOST, PORT, GROUP_ID, Maximum_threads
import extractors

threadingSemaphor = threading.Semaphore(Maximum_threads)

def handler(clientSoc, clientName):
    with threadingSemaphor:
        while True:
            try:
                # Use the socket object `clientSoc` to receive data
                requestInformation = clientSoc.recv(1024).decode()

                if requestInformation == "exit":  # Check for termination signal
                    print(f"Client {clientName} left.")
                    clientSoc.close()  # Close the socket properly
                    break

                # Process the request
                request = json.loads(requestInformation)
                Userquery = request.get('query')
                data_type = request.get('type')

                print(f"Processing request: query='{Userquery}', type='{data_type}'")
                api_url = f'https://newsapi.org/v2/{Userquery}&apiKey={API_KEY}'
                response = requests.get(api_url)

                if response.status_code != 200:
                    print(f"Error occurred: with status code {response.status_code}")
                    return

                news_data = response.json()
                file_name = f"{clientName}_{data_type}_{GROUP_ID}.json"

                # Save the raw response to a file
                with open(file_name, 'w') as json_file:
                    json.dump(news_data, json_file, indent=4)

                # Prepare response payload based on the data type requested
                if data_type == "headlines":
                    response_payload = {
                        'type': 'headlines',
                        'data': extractors.extract_headlines(news_data)[:15]
                    }
                elif data_type == "sources":
                    response_payload = {
                        'type': 'sources',
                        'data': extractors.extract_sources(news_data)[:15]
                    }
                else:
                    response_payload = {'error': 'wrong data type requested'}

                clientSoc.send(json.dumps(response_payload).encode())
            except Exception as e:
                print(f"Error handling request: {e}")
                break


def start_server():
    try:
        # Create an SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")

        # Create a socket and wrap it with SSL
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_server_socket = context.wrap_socket(server_socket, server_side=True)

        ssl_server_socket.bind((HOST, PORT))
        ssl_server_socket.listen(3)
        
        print(f"Server started on host: {HOST}, port:{PORT}")

        while True:
            clientSoc, client_address = ssl_server_socket.accept()
            clientName = clientSoc.recv(1000).decode()
            print(f"Client connected: {clientName}")
            threading.Thread(target=handler, args=(clientSoc, clientName)).start()

    except Exception as e:
        print(f"Server error: {e}")


if __name__ == "__main__":
    start_server()
