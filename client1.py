import socket 
import json

def display_menu(title, options):
    """Displays a menu with a title and its options."""
    # Print menu title and available options
    print(f"\n--- {title} ---")
    for key, value in options.items():
        print(f"{key}. {value}")
    print()

def sending_to_server(client, query, request_type):
    """Send a properly formatted request to the server."""
    try:
        # Prepare the payload with the query and type
        request_payload = {
            "query": query,
            "type": request_type
        }
        # Convert the payload to JSON format and send it to the server
        request_json = json.dumps(request_payload)
        client.send(request_json.encode('utf-8'))
    except Exception as error:
        # Handle errors that may occur during sending
        print(f"Error occurred while sending to server: {error}")