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

def process_headlines(client):
    """Manages the menu and actions for news headlines."""
    menu_options = {
        "1": "Search by Keywords",
        "2": "Search by Category",
        "3": "Search by Country",
        "4": "List All Headlines",
        "5": "Return to Main Menu"
    }
    countries = ["au", "ca", "jp", "ae", "sa", "kr", "us", "ma"]
    categories = ["business", "general", "health", "science", "sports", "technology"]

    while True:
        # Display the headlines menu
        display_menu("News Headlines", menu_options)
        user_choice = input("Select an option: ").strip()
        if user_choice == "5":
            # Return to the main menu
            break
        elif user_choice == "1":
            # Handle keyword search
            keyword = input("Enter keyword(s): ").strip()
            sending_to_server(client, f"top-headlines?q={keyword}", "headlines")
        elif user_choice == "2":
            # Handle category search
            category = input(f"Enter category ({', '.join(categories)}): ").strip().lower()
            if category not in categories:
                print("Invalid category. Please try again.")
                continue
            sending_to_server(client, f"top-headlines?category={category}", "headlines")
        elif user_choice == "3":
            # Handle country search
            country = input(f"Enter country code ({', '.join(countries)}): ").strip().lower()
            if country not in countries:
                print("Invalid country code. Please try again.")
                continue
            sending_to_server(client, f"top-headlines?country={country}", "headlines")
        elif user_choice == "4":
            # List all available headlines
            sending_to_server(client, "top-headlines?q=\" \"", "headlines")
        else:
            # Notify user of invalid input
            print("Invalid selection. Please try again.")
            continue

        # Retrieve and display server response
        response = getting_server_response(client)
        if response:
            display_data(response)
            more_details(response)

def process_sources(client):
    """Handles the menu and actions for news sources."""
    menu_options = {
        "1": "Search by Category",
        "2": "Search by Country",
        "3": "Search by Language",
        "4": "List All Sources",
        "5": "Return to Main Menu"
    }
    countries = ["au", "ca", "jp", "ae", "sa", "kr", "us", "ma"]
    languages = ["ar", "en"]
    categories = ["business", "general", "health", "science", "sports", "technology"]

    while True:
        # Display the sources menu
        display_menu("News Sources", menu_options)
        user_choice = input("Select an option: ").strip()
        if user_choice == "5":
            # Return to the main menu
            break
        elif user_choice == "1":
            # Handle category search
            category = input(f"Enter category ({', '.join(categories)}): ").strip().lower()
            if category not in categories:
                print("Invalid category. Please try again.")
                continue
            sending_to_server(client, f"top-headlines/sources?category={category}", "sources")
        elif user_choice == "2":
            # Handle country search
            country = input(f"Enter country code ({', '.join(countries)}): ").strip().lower()
            if country not in countries:
                print("Invalid country code. Please try again.")
                continue
            sending_to_server(client, f"top-headlines/sources?country={country}", "sources")
        elif user_choice == "3":
            # Handle language search
            language = input(f"Enter language code ({', '.join(languages)}): ").strip().lower()
            if language not in languages:
                print("Invalid language code. Please try again.")
                continue
            sending_to_server(client, f"top-headlines/sources?language={language}", "sources")
        elif user_choice == "4":
            # List all available sources
            sending_to_server(client, "top-headlines/sources?", "sources")
        else:
            # Notify user of invalid input
            print("Invalid selection. Please try again.")
            continue

        # Retrieve and display server response
        response = getting_server_response(client)
        if response:
            display_data(response)
            more_details(response)

def display_data(data):
    """Displays the data retrieved from the server."""
    if data.get("type") == "headlines":
        # Display a list of headlines
        print("\n--- Headlines ---")
        for idx, article in enumerate(data["data"], start=1):
            print(f"{idx}. {article['source_name']} - {article['title']}")
    elif data.get("type") == "sources":
        # Display a list of news sources
        print("\n--- Sources ---")
        for idx, source in enumerate(data["data"], start=1):
            print(f"{idx}. {source['source_name']} - {source['category']} ({source['language']}, {source['country']})")
    elif data.get("error"):
        # Display error messages if provided by the server
        print(f"\nError: {data.get('error')}")
    else:
        # Handle unexpected data formats
        print("Received an unexpected data format.")

def main():
    """Establishes the client-server connection and manages the main menu."""
    # Create a socket for client-server communication
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", 7000)  # Match the server's address and port
    client.connect(server_address)  # Connect to the server

    # Prompt user to enter a client identifier
    client_identifier = input("Enter your name: ").strip()
    client.send(client_identifier.encode('utf-8'))  # Send identifier to the server

    menu_options = {
        "1": "Explore Headlines",
        "2": "Discover Sources",
        "3": "Exit"
    }

    while True:
        # Display the main menu
        display_menu("Main Menu", menu_options)
        user_choice = input("Choose an action: ").strip()
        if user_choice == "3":
            # Exit the application
            client.send("exit".encode('utf-8'))
            print("Disconnecting...See you later!")
            break
        elif user_choice == "1":
            # Navigate to the headlines menu
            process_headlines(client)
        elif user_choice == "2":
            # Navigate to the sources menu
            process_sources(client)
        else:
            # Notify user of invalid input
            print("Invalid input. Choose a valid option.")

    # Close the client connection
    client.close()

if __name__ == "__main__":
    main()