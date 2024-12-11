import socket
import json
import requests
import threading
import extractors
from config import API_KEY, HOST, PORT, GROUP_ID,Maximum_threads 



threadingSemaphor = threading.Semaphore(Maximum_threads)
def handler(clientSoc, clientName):
    with threadingSemaphor:
        try:
            while True:
                requestInformation = clientSoc.recv(1024).decode()
                if not requestInformation or requestInformation == "exit":
                    print(f"Client {clientName} disconnected.")
                    clientSoc.close()
                    break

                # Process the request
                request = json.loads(requestInformation)
                Userquery = request.get('query')
                data_type = request.get('type')

                print(f"Processing request: query='{Userquery}', type='{data_type}'")

                api_url = f'https://newsapi.org/v2/{Userquery}&apiKey={API_KEY}'  # Construct API URL
                response = requests.get(api_url)

                if response.status_code != 200:
                    print(f"Error occurred: Status code {response.status_code}")
                    continue

                news_data = response.json()
                file_name = f"{clientName}_{data_type}_{GROUP_ID}.json"

                # Save the raw response to a file
                with open(file_name, 'w') as json_file:
                    json.dump(news_data, json_file, indent=4)

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

        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except ConnectionResetError:
            print(f"Connection reset by client {clientName}. Closing connection.")
        except Exception as e:
            print(f"An error occurred while handling client {clientName}: {e}")
        finally:
            clientSoc.close()
            print(f"Client {clientName}'s socket closed.")

def start_server():
    try:
        ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ServerSock.bind((HOST, PORT))
        ServerSock.listen(3)
        print(f"Server started on host: {HOST}, port: {PORT}")

        while True:
            try:
                clientSoc, client_address = ServerSock.accept()
                clientName = clientSoc.recv(1000).decode()
                print(f"Client connected: {clientName}")
                thread = threading.Thread(target=handler, args=(clientSoc, clientName))
                thread.start()
            except Exception as e:
                print(f"Error handling client connection: {e}")

    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        ServerSock.close()
        print("Server socket closed.")

if __name__ == "__main__":
    start_server() 
