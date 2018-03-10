# Project 7: Authenticated Brevet Time Calculator Service

## What Does This Repository Contain

The "Auth" folder contains the minimal implementation of password- and token-based which were provided for this project. Using these formats as reference, I combined these resources with my programs from project 6 to make the authenticated REST API-based service (located in the DockerRestAPI folder). This folder contains both the code needed to calculate brevet times (located in DockerMongo folder), a php file to display requested resources (located in website folder), and an api which is being used to authenticate and return the correct resources/messages (located in laptop folder). To make my api testable through a browser, I included login and register pages for users to register/sign in (located in laptop/templates).

## Recap (Project 6)

PART 1: Designing RESTful services to expose what is stored in MongoDB...

** "http://<host:port>/listAll" returns all open and close times in the database
** "http://<host:port>/listOpenOnly" returns open times only
** "http://<host:port>/listCloseOnly" returns close times only

Designed Two Different Representations: CSV and JSON (with JSON set to default): 

** "http://<host:port>/listAll/csv" returns all open and close times in CSV format
** "http://<host:port>/listOpenOnly/csv" returns open times only in CSV format
** "http://<host:port>/listCloseOnly/csv" returns close times only in CSV format
** "http://<host:port>/listAll/json" returns all open and close times in JSON format
** "http://<host:port>/listOpenOnly/json" returns open times only in JSON format
** "http://<host:port>/listCloseOnly/json" returns close times only in JSON format

Query Parameter was Also Added to Get Top "k" Open and Close Times:
(Times Were Returned In Ascending Order As Shown Below)

** "http://<host:port>/listOpenOnly/csv?top=3" returns top 3 open times only in csv
** "http://<host:port>/listOpenOnly/json?top=5" returns top 5 open times only in json

Consumer Programs Were Designed in php to Expose the Services.

## Project 7 Added Functionality

* Note that the port number for the brevet time calculator is 5003 while the port number of the authenticated REST API-based service is 5001

In order to turn project 6 (described above) into an authenticated REST API-based service, I added the following functionalities:

POST **/api/register**

- This takes the user to a register page when requested on a browser, prompting the user to enter a username and password in order to sign up
- If registration is successful, a status code of 201 is returned and the page is redirected to a new html page containing a JSON object with the newly added user and a location header containing the new user's URI 
- By JSON object with newly added user, I defined this as meaning the contents of the database for that particular user which would include 1) The username 2) The HASHED password and 3) The unique id (ie the Location/URI)
- If the username and password already exist or the user fails to enter something in one of the fields, a status code of 400 (bad request) is returned 

GET **/api/token**

Request must be authenticated using a HTTP Basic Authentication...
- This takes the user to a page prompting them to enter their username and password into two input fields (ie a login page)
- Upon submitting their username and password, the program checks the database to make sure their username and password are valid (using psw.py)
- If users credentials are valid, a token is made using the secret key and the users unique id (using createToken.py). This token is then returned as a json object
- The returned JSON object (with 201 status code) should contain 1) The token itself & 2) The duration of the token - CURRENTLY SET TO 30 SECONDS
- To obtain the desired resources, this token should be copied and pasted into the header of the next request as shown below:

http://127.0.0.1:5001/listAll?token=eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMDY0MzE2NiwiZXhwIjoxNTIwNjQzMTk2fQ.eyJpZCI6IjVhYTMyYzNlNTc0MWM1MDA0OTIyODMyMCJ9.olcjG8VkKYMsHlaTdKV-0K0bbZoEZo5Thfirxmqpz68

- In this case, your token is eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMDY0MzE2NiwiZXhwIjoxNTIwNjQzMTk2fQ.eyJpZCI6IjVhYTMyYzNlNTc0MWM1MDA0OTIyODMyMCJ9.olcjG8VkKYMsHlaTdKV-0K0bbZoEZo5Thfirxmqpz68

- If the user is not in the data base or their credentials are not valid or one of the input fields is left blank, then a status code of 401 (unauthorized) is returned

GET **/RESOURCE-YOU-CREATED-IN-PROJECT-6**

- If request is authenticated using token-based authentication (explained above), a protected <resource> (created in project 6 and explained above) is returned
- If the token needed to access this protected resource is not valid or not given, a status code 401 (unauthorized) is returned

## Tasks

You'll turn in your credentials.ini using which we will get the following:

* The working application with three parts.

* Dockerfile

* docker-compose.yml
