import requests, sys
import threading
import time
port = int(sys.argv[1])
half_link = "http://127.0.0.1:" + str(port)

#GET methods are here 


def req():
	URL = half_link + "/file1.html"				#This source exist.
	r = requests.get(url = URL)
	r = str(r)
	if (r == '<Response [200]>'):
		print("Query->0(GET) Status Code : 200")
	else:
		print("Query->0(GET) Status Code : 404")
def req1():
	URL1 = half_link + "/sahil/gaurav/prem/new_html.html" 	#This source doesn't exist.
	r1 = requests.get(url = URL1)
	r1 = str(r1)
	if (r1 == '<Response [200]>'):
		print("Query->1(GET) Status Code : 200")
	else:
		print("Query->1(GET) Status Code : 404")
def req2():
	URL2 = half_link + "/gaurav"				#This source exist and it is a Directory.
	r2 = requests.get(url = URL2)
	r2 = str(r2)
	if (r2 == '<Response [200]>'):
		print("Query->2(GET) Status Code : 200")
	else:
		print("Query->2(GET) Status Code : 404")
def req3():
	URL3 = half_link + "/putted.html"			#This source exist.
	r3 = requests.get(url = URL3)
	r3 = str(r3)
	if (r3 == '<Response [200]>'):
		print("Query->3(GET) Status Code : 200")
	else:
		print("Query->3(GET) Status Code : 404")
def req4():
	URL4 = half_link + "/prem.png"				#This source exist and it is a binary file.
	r4 = requests.get(url = URL4)
	r4 = str(r4)
	if (r4 == '<Response [200]>'):
		print("Query->4(GET) Status Code : 200")
	else:
		print("Query->4(GET) Status Code : 404")
def req5():
	URL5 = half_link + "/gaurav/index.html"			#This source exist.
	r5 = requests.get(url = URL5)
	r5 = str(r5)
	if (r5 == '<Response [200]>'):
		print("Query->5(GET) Status Code : 200")
	else:
		print("Query->5(GET) Status Code : 404")

#POST methods are here

def p():							#Only Text data is there 
	session = requests.Session()
	half_link = "http://127.0.0.1:" + str(port)
	URL6 = half_link + '/new_form.html'
	myObj = {'f_name':'Gaurav_Python', 'l_name':'Wawdhane_Python', 'u_name':'gaurav123', 'pass':'Gaurav', 'name':'Sahil_Wawdhane'}
	r6 = session.post(url = URL6, data = myObj)
	r6 = str(r6)
	if (r6 == '<Response [200]>'):
		print("Query->0(POST) Status Code : 200 ---> File Created")
	else:
		print("QUery->0(POST) Status Code : 404")

def p1():							#Text Data + one text file
	session = requests.Session()
	half_link = "http://127.0.0.1:" + str(port)
	URL6 = half_link + '/new_form.html'
	myObj = {'f_name':'Gaurav_Python', 'l_name':'Wawdhane_Python', 'u_name':'gaurav123', 'pass':'Gaurav', 'name':'Sahil_Wawdhane'}
	r6 = session.post(url = URL6, data = myObj)
	r6 = str(r6)
	if (r6 == '<Response [200]>'):
		print("Query->1(POST) Status Code : 200 ---> File Created")
	else:
		print("QUery->1(POST) Status Code : 404")

def p2():								#Text data + two files (One binary and one text file)
	session = requests.Session()
	half_link = "http://127.0.0.1:" + str(port)
	URL6 = half_link + '/new_form.html'
	myObj = {'f_name':'Gaurav_Python', 'l_name':'Wawdhane_Python', 'u_name':'gaurav123', 'pass':'Gaurav', 'name':'Sahil_Wawdhane'}
	r6 = session.post(url = URL6, data = myObj)
	r6 = str(r6)
	if (r6 == '<Response [200]>'):
		print("Query->2(POST) Status Code : 200 ---> File Created")
	else:
		print("QUery->2(POST) Status Code : 404")


def d1():								#Deleting a file which is there on the server or may be deleted
	half_link = "http://127.0.0.1:" + str(port)
	url_temp = half_link + '/prem.pdf'
	x = requests.delete(url_temp, auth = ('gaurav', 'Gaurav123'))
	x = str(x)
	if (x == '<Response [404]>'):
		print('Query->1(DELETE) Status Code : 404')
	elif (x == '<Response [403]>'):
		print('Query->1(DELETE) Status Code : 403 Authorization Required')
	elif (x == '<Response [401]>'):
		print('Query->1(DELETE) Status Code : 401 Unauthorized Client')
	else:
		print('Query->1(DELETE) Status Code : 200 Resource Deleted')

def d2():								#Deleting a file which is on the server or may be deleted
	half_link = "http://127.0.0.1:" + str(port)
	url_temp = half_link + '/prem.pdf'
	x = requests.delete(url_temp, auth = ('gaurav', 'Gaurav123'))
	x = str(x)
	if (x == '<Response [404]>'):
		print('Query->2(DELETE) Status Code : 404')
	elif (x == '<Response [403]>'):
		print('Query->2(DELETE) Status Code : 403 Authorization Required')
	elif (x == '<Response [401]>'):
		print('Query->2(DELETE) Status Code : 401 Unauthorized Client')
	else:
		print('Query->2(DELETE) Status Code : 200 Resource Deleted')


def d3():								#Deleting a file for Unauthorized Client
	half_link = "http://127.0.0.1:" + str(port)
	url_temp = half_link + '/prem.pdf'
	x = requests.delete(url_temp, auth = ('gaurav', 'Gau123'))
	x = str(x)
	if (x == '<Response [404]>'):
		print('Query->3(DELETE) Status Code : 404')
	elif (x == '<Response [403]>'):
		print('Query->3(DELETE) Status Code : 403 Authorization Required')
	elif (x == '<Response [401]>'):
		print('Query->3(DELETE) Status Code : 401 Unauthorized Client')
	else:
		print('Query->3(DELETE) Status Code : 200 Resource Deleted')


def h1():								#File is present on the Server
	half_link = "http://127.0.0.1:" + str(port)
	url = half_link + '/file1.html'
	x = requests.head(url)
	x = str(x)
	if (x == '<Response [200]>'):
		print('Query->1(HEAD) Status Code: 200 OK')
	else:
		print('Query->1(HEAD) Status Code : 404 Not Found')



def h2():								#File is present on the Server
	half_link = "http://127.0.0.1:" + str(port)
	url = half_link + '/file2.html'
	x = requests.head(url)
	x = str(x)
	if (x == '<Response [200]>'):
		print('Query->2(HEAD) Status Code: 200 OK')
	else:
		print('Query->2(HEAD) Status Code : 404 Not Found')

def h3():								#File is not present on the Server
	half_link = "http://127.0.0.1:" + str(port)
	url = half_link + '/file1/file1.html'
	x = requests.head(url)
	x = str(x)
	if (x == '<Response [200]>'):
		print('Query->3(HEAD) Status Code: 200 OK')
	else:
		print('Query->3(HEAD) Status Code : 404 Not Found')

def put1():							#Creating a new file for PUT request
	half_link = "http://127.0.0.1:" + str(port)
	f_open = open('new_form.html', 'rb')
	payload = f_open.read()
	url = half_link + '/gaurav/sahil/put2.html'
	x = requests.put(url, data=payload, auth = ('gaurav', 'Gaurav123'))
	x = str(x)
	if (x == '<Response [201]>'):
		print('Query->0(PUT) Status Code : 201 Created')
	
def put2():							#Creating a new Binary file for PUT request
	half_link = "http://127.0.0.1:" + str(port)
	f_open = open('test.jpg', 'rb')
	payload = f_open.read()
	url = half_link + '/gaurav/sahil/prem.jpg'
	x = requests.put(url, data=payload, auth = ('gaurav', 'Gaurav123'))
	x = str(x)
	if (x == '<Response [201]>'):
		print('Query->0(PUT) Status Code : 201 Created')
	


get_thread = threading.Thread(target=req, args=())
get_thread.start()
get_thread = threading.Thread(target=req1, args=())
get_thread.start()
get_thread = threading.Thread(target=req2, args=())
get_thread.start()
get_thread = threading.Thread(target=req3, args=())
get_thread.start()
get_thread = threading.Thread(target=req4, args=())
get_thread.start()
get_thread = threading.Thread(target=req5, args=())
get_thread.start()
post_thread = threading.Thread(target=p, args=())
post_thread.start()
post_thread = threading.Thread(target=p1, args=())
post_thread.start()
post_thread = threading.Thread(target=p2, args=())
post_thread.start()
delete_thread = threading.Thread(target=d1, args=())
delete_thread.start()
delete_thread = threading.Thread(target=d2, args=())
delete_thread.start()
delete_thread = threading.Thread(target=d3, args=())
delete_thread.start()
head_thread = threading.Thread(target=h1, args=())
head_thread.start()
head_thread = threading.Thread(target=h2, args=())
head_thread.start()
head_thread = threading.Thread(target=h3, args=())
head_thread.start()
put_thread = threading.Thread(target=put1, args=())
put_thread.start()
put_thread = threading.Thread(target=put2, args=())
put_thread.start()
