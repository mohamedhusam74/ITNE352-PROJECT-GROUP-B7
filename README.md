# ITNE352-PROJECT-GROUP-B7

# Project Title
Real-Time News Aggregation System with Interactive Client-Server Communication

## Project Description
The goal of this project is to create a real-time news aggregation system that uses an interactive client-server architecture to give consumers access to the most recent news sources and headlines. The system uses the NewsAPI to retrieve and present current content that is customized for the user, including news that has been filtered by keywords, categories, nations, or languages.

With the help of the client application's simple design, users may browse menus, look at news headlines, and investigate news sources. After processing client queries, the server interacts with the NewsAPI to retrieve the necessary information and provides the client with structured responses. The project places a strong emphasis on user-focused design, effective server-client communication, and dynamic data retrieval.

## Semester
1st semester 2024-2025

## Group Information
- **Group Name:** B7
- **Course Code:** ITNE352
- **Section:** 1
- **Student Names:** Mohamed Husam Darwish , Ziyad Abdulnoor Yousif
- **Student IDs:** 202208375 ,  202200178 

---

## Table of contents:
1. [Requirements](#requirements)
2. [How to Run the System](#how-to-run-the-system)
3. [Scripts](#scripts)
4. [Additional Concepts](#additional-concepts)
5. [Acknowledgments](#acknowledgments)
6. [Conclusion](#conclusion)
7. [Resources](#resources-optional)

## Requirments: 
1. Install python in VScode to be able to run the scripts

2. Install a requests module

3. Get your api key from "News API"
   
## How to Run the System
1. Download the client file and the three files of the server
2. Then to run open one terminal for the server and another one for the client
3. To run the server type "python server_file.py" in the trerminal and it will start to listen to the client connection
4. To run the client type "python client1.py" then:
   - Enter your user name
   - Making requests will be from the menu
   - After finishing, click "quit" to terminate 
---

## Scripts

1. **Client-Side Scripts:**
   ![first 25 lines](https://github.com/user-attachments/assets/25f16d38-bf50-4451-8702-f93d3f33ceb2)

   The client script is to send requests to the server about specific news with different country, category etc... First function is the "revealing_menu" which 
   uses the title and options to show the main menu with the title and its available options, it also has two parameters. While the seconf function 
  "sending_to_server" is used to send a formated request to the server, it has three parameters client, query and request_type. For the packages e used Socket and 
   json. 

   
 
3. **Server-Side Scripts:**
   
![image](https://github.com/user-attachments/assets/bf96074c-08aa-4d69-b17d-0260e623a95a)

The server will be used to recieve requests from the client. For the server script, I made 3 files for the server code, configration and the expector. first function handler is used to Handles communication with a connected client and it contains 2 paremeters which are clientSoc, clientName, the clientSoc is the Socket object for client communication and clientName for the name of the connected client. Were we used the socket, json, requests, threading and extractors as the packages. 


---

## Additional concept
For additional concept we used SSL


![image](https://github.com/user-attachments/assets/77ec45d2-57e8-440a-851e-de9d52eae4cc)

![image](https://github.com/user-attachments/assets/96a2d6ff-e3fc-4e20-8f47-96d72744e5a1)

![image](https://github.com/user-attachments/assets/b1d633fd-f288-481e-82bd-b44efb9e141b)
These photos are with encryption with ssl




------------------------------------------------------------------------------------------------

![image](https://github.com/user-attachments/assets/ea23acbf-f39f-47f7-a8b6-204c35c4e1b4)

![image](https://github.com/user-attachments/assets/4f975b27-1ad1-438e-ac41-5901344e98d7)

![image](https://github.com/user-attachments/assets/bff76282-bc69-4221-a5b4-4f9c7cb68df0)
These photos are without encryption with ssl


So we have three pictures before encryption
and also three picture after encryption




## Acklonegment
It was a very intresting course were we have acheived valuble knowledge about programming especally python. Special thank to Dr. Mohd Almeer who really deserves this "thank" for giving us some of his valuable knowledge and educating us in the network major.    

# Conclution:
To conclude, this project offers an interactive client-server real-time news aggregation system. It delivers the most recent headlines based on user selections, including keywords, categories, countries, and languages, using the NewsAPI.


