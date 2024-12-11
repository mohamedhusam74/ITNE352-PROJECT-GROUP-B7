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

def getting_server_response(client):
    """Fetch and save the server's response."""
    try:
        # Receive data from the server
        response_data = client.recv(8192).decode('utf-8')
        if not response_data:
            # Handle cases where the server sends no data
            print("Server sent an empty response.")
            return None
        # Decode the JSON response into a Python dictionary
        return json.loads(response_data)
    except json.JSONDecodeError as json_error:
        # Handle errors in JSON decoding
        print(f"Error decoding server response as JSON: {json_error}")
        return None
    except Exception as error:
        # Handle general errors while receiving the response
        print(f"Error occurred while receiving response: {error}")
        return None

def more_details(data):
    """Asks the user if they want more details about any returned item and displays additional information."""
    while True:
        # Ask the user if they want more details
        user_input = input("\nDo you want more details about any item? Enter the number (or 'no' to skip): ").strip().lower()
        if user_input == "no":
            break

        if user_input.isdigit():
            # Validate and parse user input for item details
            index = int(user_input) - 1
            if data.get("type") == "headlines" and 0 <= index < len(data["data"]):
                # Display details for a selected headline
                item = data["data"][index]
                print(f"\n--- Details for Headline {index + 1} ---")
                print(f"Source Name: {item.get('source_name', 'N/A')}")
                print(f"Author: {item.get('author', 'N/A')}")
                print(f"Title: {item.get('title', 'N/A')}")
                print(f"URL: {item.get('url', 'N/A')}")
                print(f"Description: {item.get('description', 'N/A')}")
                print(f"Publish Date: {item.get('publish_date', 'N/A')}")
                print(f"Publish Time: {item.get('publish_time', 'N/A')}")
            elif data.get("type") == "sources" and 0 <= index < len(data["data"]):
                # Display details for a selected source
                item = data["data"][index]
                print(f"\n--- Details for Source {index + 1} ---")
                print(f"Source Name: {item.get('source_name', 'N/A')}")
                print(f"Country: {item.get('country', 'N/A')}")
                print(f"Description: {item.get('description', 'N/A')}")
                print(f"URL: {item.get('url', 'N/A')}")
                print(f"Category: {item.get('category', 'N/A')}")
                print(f"Language: {item.get('language', 'N/A')}")
            else:
                # Handle invalid selection
                print("Invalid selection. Please try again.")
        else:
            # Notify user about invalid input
            print("Invalid input. Please enter a valid number or 'no'.")