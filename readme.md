

This is an http Server Project

step 1:	Run the server.py file as 'python3 server.py'
	(This will run the file on port number 5555 defined in gaurav.conf file)

step 2: Run the auto-testing file (location : test_py/multi_server.py) as 'python multi_server.py'

step 3: Check the output on the terminal of the file multi_server.py
step 4: The outputs are status code related to the various request

(All the requests are there in the access.log file and errors are in the error.log file)


1) server.py is the main file to start the server
2) You can change the document root , serverroot , port number etc. in the gaurav.conf file
3) Currently htmlFiles is the document root for the server
4) The logs files are stored into the direcorty logs whose locations are specified in the configure file


running in Linux Terminal:
>python3 server.py

This project includes the GET, HEAD, POST, PUT, DELETE Method.

GET method can be done using any browser by sending the headers on the required port number on localhost.

HEAD method can be done using postman.

POST method can be done using any form in the browser.

PUT method is for uploading any resource on the server. This method requires basic authorization(can be done in Postman)

DELETE method is for deleting any resource on the server. This method requires basic authorizaton(can be done in Postman)
