#!/usr/bin/python
import socket
import mimetypes
import sys
import glob
import time
import os.path
import datetime
import re
import threading
import configparser
import base64
import random


client_list = []


def cookie_value ():
	s = ''
	for i in range(0, 10):
		if (i % 3 == 0):
			i_random = random.randint(65, 90)
			i_random = chr(i_random)
		else:
			i_random = random.randint(0,100)
			i_random = str(i_random)
		s += i_random
	return s

def cookie_check (request_head):
	cook = 'Cookie'
	s = ''
	s_file = ''
	if cook not in request_head:
		s += 'Set-Cookie: user_id='
		cook_value = cookie_value()
		s += cook_value
		s_file = 'user_id = ' + cook_value
		s += '\n'
		s_file += '; '
		s_file += 'Expires='
		Next_Date = datetime.datetime.today() + datetime.timedelta(days=10)
		s_file += time.strftime("%a, %d %b %Y %H:%M:%S GMT", Next_Date.timetuple())
		s_file += '; Secure; HttpOnly; remember_me=true\n'
		s_file += 'User-Agent : ' 
		s_file += request_head['User-Agent']
		s_file += '\n\n'
		f_cookie_path = serverroot['serverroot'] + '/cookie.log'
		f_cookie = open(f_cookie_path, 'a+')
		f_cookie.write(s_file)
		f_cookie.close()
	return s
	
			
def temp_post_method(connectionSocket, sentence):
	global access_log
	sentence_get = sentence.split(b'\r\n\r\n')
	sentence_get = sentence_get[0]
	sentence = sentence.split(b'\r\n')
	server_root = serverroot['serverroot']
	if (not os.path.isdir(server_root + '/uploads')):
		os.mkdir(server_root + '/uploads')
	multipart_data = 1
	for text in sentence:
		if (text.find(b'Content-Type') == 0):
			text = text.decode()
			text = text.split(':')
			if (text[1] == ' application/x-www-form-urlencoded'):
				data_text = sentence[len(sentence) - 1]
				temp_file_name = server_root + '/uploads/data.log'
				fp = open(temp_file_name, 'a+')
				data_text = data_text.decode()
				for word in data_text:
					if (word == '&'):
						fp.write(' & ')
					else:
						fp.write(word)
				multipart_data = 0
				fp.write("\n")
				fp.close()
	if (multipart_data == 1):
		file_count = 1
		i = 0
		index_list = []
		for text in sentence:
			if (text.find(b'Content-Disposition') == 0):
				index_list.append(i)
			i = i + 1
		temp_i = index_list[0]
		folder_name = sentence[temp_i - 1]
		folder_name = folder_name.decode()
		len_folder_name = len(folder_name)
		len_folder_name = len_folder_name - 10
		folder_name = folder_name[len_folder_name:]
		folder_name = server_root + '/uploads/' + folder_name
		while (os.path.isdir(folder_name)):
			folder_name = folder_name + str(random.randint(0,1000))
		os.mkdir(folder_name)
		file_name_data = folder_name + '/data.log'
		fp = open(file_name_data, "w")
		for i in index_list:
			text = sentence[i]
			text = text.decode()
			new_text = text.split(';')
			try:
				id_name = new_text[1]
				id_name = id_name.split('="')
				id_name = id_name[1]	
				id_name = id_name[:-1]
				file_name = new_text[2]
				file_name = file_name.split('="')
				file_name = file_name[1]
				file_name = file_name[:-1]
				if (file_name != ''):
					file_name = folder_name + '/' + id_name + "_" + file_name
					fp1 = open(file_name, "wb")
					fp1.write(sentence[i+3])
					fp1.close()
			except:
				new_data_text = sentence[i].decode()
				new_data_text = new_data_text.split(';')
				fp.write(new_data_text[1])
				fp.write (' & ')
				fp.write(sentence[i+2].decode())
				fp.write("\n")				
		fp.close()
	f_access = open(access_log['access'], 'a+')
	request_head = dict()
	sentence_get = sentence_get.decode()
	sentence = sentence_get.split('\r\n')
	for line in sentence:
		words_new = line.split(':')
		try:
			request_head[words_new[0]] = words_new[1]
		except:
			continue
	file_name = sentence[0].split()
	req = 'GET ' + file_name[1] + ' HTTP/1.1'
	req = req + '\r\n' 
	for i in range(1, len(sentence)):
		req += sentence[i]
		req += '\r\n'
	req = req.encode()
	access_text = request_head['Host']
	access_text += '- -'
	access_text += time.strftime("[%d/%b/%Y:%H:%M:%S +5:30] ", time.localtime())
	access_text += '"' + sentence[0] + '" ' + '200' + ' '
	access_text += " " + '"' + '"' + '-'
	access_text += ' "'
	access_text += request_head['User-Agent']
	access_text += '"\n'
	f_access.write(access_text)
	f_access.close()
	#client_list.remove(connectionSocket)
	getHead_method(connectionSocket, req)

    
def getHead_method(connectionSocket, sentence):
	sentence = sentence.decode()
	refresh_status = 0
	dir_indexhtml = 0
	img_check = 0
	global documentRoot
	global access_log
	request_head = dict()
	line_seprate = sentence.split('\r\n')
	for line in line_seprate:
		words_new = line.split(':')
		try:
			s = ''
			for i in range(1, len(words_new)):
				s += words_new[i]
			request_head[words_new[0]] = s
		except:
			continue
	f_access = open(access_log['access'], 'a+')
	f_error =open(error_log['error'], 'a+')
	words = sentence.split()
	if_modified = sentence.split('\r\n')
	if_modified_date = if_modified[len(if_modified)-3]
	if_modified_date = if_modified_date.split(': ')
	if (if_modified_date[0] == 'If-Modified-Since'):
		date_if_modified = if_modified_date[1]
		ifModified_obj = datetime.datetime.strptime(date_if_modified, '%a, %d %b %Y %H:%M:%S GMT')
		#print('IF-MODIFIED : ' + str(ifModified_obj))
		refresh_status = 1
	file_name = words[1][1::]
	document_root = documentRoot['documentRoot']
	old_file_name = file_name
	file_name = document_root + '/' + file_name
	if (file_name == ''):
		try:
			f = open('index.html')
			get_time = time.ctime(os.path.getmtime('index.html'))
			text = f.read()
			f.close()
			st_code = 200
			string = 'HTTP/1.1 200 OK\n'
		except:
			string = 'HTTP/1.1 404 Not Found\n'
			f = open('bad_request.html')
			get_time = time.ctime(os.path.getmtime('bad_request.html'))
			st_code = 404
			text = f.read()
			f.close()
	else:
		if (os.path.isfile(file_name)):
			try:
				string = 'HTTP/1.1 200 OK\n'
				st_code = 200
				if(file_name.split('.')[1] == 'html' or file_name.split('.')[1] == 'htm' or file_name.split('.')[1] == 'txt'):
					f = open(file_name)
				else:
					f = open(file_name, 'rb')
					img_check = 1
				get_time = time.ctime(os.path.getmtime(file_name))
				text = f.read()
				f.close()
			except:
				f = open('bad_request.html')
				st_code = 404
				get_time = time.ctime(os.path.getmtime('bad_request.html'))
				string = 'HTTP/1.1 404 Not Found\n'
				text = f.read()
				f.close()
		else:
			if (os.path.isdir(file_name)):
				files_in_dir = os.listdir(file_name)
				for files in files_in_dir:
					if (files == 'index.html'):
						dir_indexhtml = 1
						string = 'HTTP/1.1 200 OK\n'
						st_code = 200
						file_new_name = file_name + '/index.html'
						f = open(file_new_name, 'r')
						text = f.read()
						f.close()
						break
				if (dir_indexhtml == 0):
					st_code = 200
					string = 'HTTP/1.1 200 OK\n'
					text = '<!DOCTYPE html><html><head><title>Directory</title></head><body><ul>'
					for files in files_in_dir:
						new_file_name = old_file_name + '/' + files
						text += '<li><a href ="' + new_file_name + '">' + files + '</a></li>'
					text += '</ul></body></html>'
			else:
				string = 'HTTP/1.1 404 Not Found\n'
				st_code = 404
				f = open('bad_request.html')
				get_time = time.ctime(os.path.getmtime('bad_request.html'))
				text = f.read()
				f.close()
	if not os.path.isdir(file_name):
		mod_time = get_time.split()
		lastModified = mod_time[0] + ', ' + mod_time[2] + ' ' + mod_time[1] + ' ' + mod_time[4] + ' ' + mod_time[3] + ' GMT'
		lastModified_obj = datetime.datetime.strptime(lastModified, '%a, %d %b %Y %H:%M:%S GMT')
		if (refresh_status == 1):
			if (lastModified_obj <= ifModified_obj):
				string = 'HTTP/1.1 304 Not Modified\n'
				st_code = 304
	string += 'Date: '
	string += time.strftime("%a, %d %b %Y %H:%M:%S GMT\n", time.localtime())
	string += "Server: Gaurav's Server/1.0.0(Win32)\n"
	string += 'Content-Length:'
	if (img_check == 0):
		string += str(len(text.encode('utf-8')))
		string += '\n'
		string += 'Content-Type: text/html\n'
	else:
		string += str(len(text))
		string += '\n'
		string += 'Content-Type: '
		string += mimetypes.guess_type(file_name)[0]
		string += '\n'
	if (not os.path.isdir(file_name)):
		string += 'Last-Modified: '
		string += lastModified + '\n'
	string += str(cookie_check(request_head))
	string += 'charset=UTF-8\n\n'
	if (words[0] == 'GET' and os.path.isfile(file_name)):
		if (refresh_status == 0):
			if (img_check == 0):
				string = string + text
			else:
				string = bytes(string, 'utf-8') + text
		else:
			if (lastModified_obj > ifModified_obj):
				if (img_check == 0):
					string = string + text
				else:
					string = bytes(string, 'utf-8') + text
	elif(words[0] == 'GET'):
		if (img_check == 0):
			string = string + text
		else:
			string = bytes(string, 'utf-8') + text
	else:
		string = string
	access_text = request_head['Host']
	access_text += '- -'
	access_text += time.strftime("[%d/%b/%Y:%H:%M:%S +5:30] ", time.localtime())
	access_text += '"' + words[0] + ' ' + words[1] + ' HTTP/1.1' + '" ' + str(st_code) + ' ' + str(len(text))
	access_text += " " + '"' + '"' + '-'
	access_text += ' "'
	access_text += request_head['User-Agent']
	access_text += '"\n'
	f_access.write(access_text)
	if (st_code == 404):
		f_error.write(access_text)
	f_error.close()
	f_access.close()
	client_list.remove(connectionSocket)
	#print(string)
	if (img_check == 0):
		connectionSocket.send(string.encode())
	else:
		connectionSocket.send(string)


def delete_method(connectionSocket, sentence):
	sentence = sentence.decode()
	permission_allowed = 0
	global documentRoot
	global userinfo
	global access_log
	request_head = dict()
	line_seprate = sentence.split('\r\n')
	for line in line_seprate:
		words_new = line.split(':')
		try:
			request_head[words_new[0]] = words_new[1]
		except:
			continue
	f_access = open(access_log['access'], 'a+')
	f_error =open(error_log['error'], 'a+')
	words = sentence.split()
	auths = sentence.split('\r\n')
	for auth in auths:
		if (auth == ''):
			break
		auth_words = auth.split()
		try:
			if(auth_words[0] == "Authorization:"):
				break
		except:
			continue
	if (auth_words[0] == "Authorization:"):
		temp = base64.b64decode(auth_words[2])
		temp = temp.decode('utf-8')
		auth_per = userinfo['loginid'] + ':' + userinfo['password']
		if (temp == auth_per):
			permission_allowed = 1
		else:
			string = 'HTTP/1.1 401 Unauthorized client\n\n'
			st_code = 200
			text = '<!DOCTYPE html><html><body><h1>Authorization failed(Username or Password is wrong) </h1></body></html>'
			string += text
	else:
		string = 'HTTP/1.1 403 Forbidden\n\n'
		st_code = 200
		text = '<!DOCTYPE html><html><body><h1>Authorization Required </h1></body></html>'
		string += text
	if (permission_allowed == 1):
		try:
			file_name = words[1][1::]
			file_name = documentRoot['documentRoot'] + '/' + file_name
			if (os.path.isfile(file_name)):
				st_code = 200
				os.remove(file_name)
				string = 'HTTP/1.1 200 OK\n'
				string += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\n", time.localtime())
				string += "Server: Gaurav's Server/1.0.0(Win32)\n"
				string += 'Content-type:text/html\n'
				string += str(cookie_check(request_head))
				string += 'Content-length:'
				string += '30'
				string += 'Connection:Closed\n\n'
				string += "<html><body><h1>URL Deleted</h1></body></html>"
			else:
				st_code = 404
				string = 'HTTP/1.1 404 Not Found\n'
				string += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\n", time.localtime())
				string += "Server: Gaurav's Server/1.0.0(Win32)\n"
				string += 'Content-type:text/html\n'
				string += 'Content-length:'
				f = open('bad_request.html')
				text = f.read()
				f.close()
				string += str(len(text.encode('utf-8')))
				string += '\n'
				string += 'Connection:Closed\n\n'
				string += text
		except Exception as e:
			print(e)
	access_text = request_head['Host']
	access_text += '- -'
	access_text += time.strftime("[%d/%b/%Y:%H:%M:%S +5:30] ", time.localtime())
	if (st_code == 200):
		con_length = '30'
	else:
		con_length = str(len(text.encode('utf-8')))
	access_text += '"' + words[0] + ' ' + words[1] + ' HTTP/1.1' + '" ' + str(st_code) + ' ' + con_length
	access_text += " " + '"' + '"' + '-'
	access_text += ' "'
	access_text += request_head['User-Agent']
	access_text += '"\n'
	f_access.write(access_text)
	if (st_code == 404):
		f_error.write(access_text)
	f_access.close()
	f_error.close()
	client_list.remove(connectionSocket)
	connectionSocket.send(string.encode())


def put_method(connectionSocket, sentence):
	file_check = 1
	sentence_new = sentence.split(b'\r\n\r\n')
	words_new = sentence_new[0].decode().split('\r\n')
	for word in words_new:
		new_word = word.split(':')
		if (new_word[0] == "Content-Type"):
			if (new_word[1] == "text/html"):
				file_check = 0
			else:
				file_check = 1
			break
	sentence = sentence_new[0].decode()
	permission_allowed = 0
	global userinfo
	global documentRoot
	global access_log
	request_head = dict()
	line_seprate = sentence.split('\r\n')
	for line in line_seprate:
		words_new = line.split(':')
		try:
			request_head[words_new[0]] = words_new[1]
		except:
			continue
	f_access = open(access_log['access'], 'a+')
	auths = sentence.split('\r\n')
	for auth in auths:
		if (auth == ''):
			break
		auth_words = auth.split()
		try:
			if(auth_words[0] == "Authorization:"):
				break
		except:
			continue
	if (auth_words[0] == "Authorization:"):
		temp = base64.b64decode(auth_words[2])
		temp = temp.decode('utf-8')
		auth_per = userinfo['loginid'] + ':' + userinfo['password']
		if (temp == auth_per):
			permission_allowed = 1
		else:
			string = 'HTTP/1.1 401 Unauthorized client\n'
			string += 'Content-type: text/html\n\n'
			st_code = 401
			text = '<!DOCTYPE html><html><body><h1>Authorization failed(Username or Password is wrong) </h1></body></html>'
			string += text
			con_length = len(text)
	else:
		string = 'HTTP/1.1 403 Forbidden\n'
		string += 'Content-type: text/html\n\n'
		st_code = 403
		text = '<!DOCTYPE html><html><body><h1>Authorization Required </h1></body></html>'
		con_length = len(text)
		string += text
	if (permission_allowed == 1):
		#words = re.split('\n\n|\r\n\r\n|\r\n\n|\n\n\r|\n\r\n|\n\r\n\r', sentence)
		#text = words[1]
		text = sentence_new[1]
		cu_dir = documentRoot['documentRoot']
		words = sentence.split()
		file_name = words[1][1::]
		if (file_name == ''):
			file_name = 'index.html'
		word = file_name.split('/')
		word.remove(word[len(word) - 1])
		print(os.path.isfile(file_name))
		if(os.path.isfile(file_name)):
			st_code = 200
		else:
			st_code = 201
			for wrd in word:
				cu_dir += '/'
				cu_dir += wrd
				if (not os.path.isdir(cu_dir)):
					os.mkdir(cu_dir)
		file_name = documentRoot['documentRoot'] + '/' + file_name
		if (file_check == 0):
			fp = open(file_name, 'w+')
			fp.write(text.decode())
		else:
			fp = open(file_name, 'wb')
			fp.write(bytes(text))
		fp.close()
		string = 'HTTP/1.1 ' +  str(st_code)
		if (st_code == 201):
			string += ' Created\n' 
		if (st_code == 200):
			string += ' OK\n'
		string += 'Content-type: text/html\n\n'
		text = '<!DOCTYPE html><html><head><title>File Modified</title></head><body><center><h1>URI Modified</h1></center></body></html>'
		con_length = len(text)
		string += text
	if (permission_allowed == 0):
		words = sentence.split()
	access_text = request_head['Host']
	access_text += '- -'
	access_text += time.strftime("[%d/%b/%Y:%H:%M:%S +5:30] ", time.localtime())
	access_text += '"' + words[0] + ' ' + words[1] + ' HTTP/1.1' + '" ' + str(st_code) + ' ' + str(con_length)
	access_text += " " + '"' + '"' + '-'
	access_text += ' "'
	access_text += request_head['User-Agent']
	access_text += '"\n'
	f_access.write(access_text)
	f_access.close()
	client_list.remove(connectionSocket)
	connectionSocket.send(string.encode())


def default_method (connectionSocket, text):
	text = text.decode()
	request_head = dict()
	global access_log
	f_access = open(access_log['access'], 'a+')
	f_error =open(error_log['error'], 'a+')
	st_code = 405
	words = text.split('\r\n')
	for word in words:
		new_word = word.split(':')
		try:
			request_head[new_word[0]] = new_word[1]
		except:
			continue
	text = '<!DOCTYPE html><html><head><title>Method Not Allowed</title></head><body><h1>Method Not Allowed</h1></body></html>'
	access_text = request_head['Host']
	access_text += '- -'
	access_text += time.strftime("[%d/%b/%Y:%H:%M:%S +5:30] ", time.localtime())
	access_text += '"' + words[0] + ' HTTP/1.1' + '" ' + str(st_code) + ' ' + str(len(bytes(text, 'utf-8')))
	access_text += " " + '"' + '"' + '-'
	access_text += ' "'
	access_text += request_head['User-Agent']
	access_text += '"\n'
	f_access.write(access_text)
	f_error.write(access_text)
	f_error.close()
	f_access.close()
	string = 'HTTP/1.1 405 Method Not allowed\n'
	string += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\n", time.localtime())
	string += "Server: Gaurav's Server/1.0.0(Win32)\n"
	string += 'Content-type: text/html\n'
	string += 'Content-length: '
	string += str(len(bytes(text, 'utf-8')))
	string += '\nLast-Modified :'
	string += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\n", time.localtime())
	string += '\n\n'
	string += text
	client_list.remove(connectionSocket)
	connectionSocket.send(string.encode())

def new_receive(connectionSocket):
	sentence = connectionSocket.recv(1024)
	text = sentence
	sentence = sentence.split(b'\r\n\r\n')
	header_len = len(sentence[0])
	words = sentence[0].decode().split()
	new_words = sentence[0].decode().split('\r\n')
	for word in new_words:
		word = word.split(':')
		if (word[0] == 'Content-Length'):
			length = word[1]
			length = int(length) + header_len
			break
	try:
		if (words[0] == 'GET'):
			getHead_method(connectionSocket, text)
		elif (words[0] == 'HEAD'):
			getHead_method(connectionSocket, text)
		elif (words[0] == 'DELETE'):
			delete_method(connectionSocket, text)
		elif (words[0] == 'PUT'):
			length = int(length)
			length = length - 1024
			while (length > 0):
				text += connectionSocket.recv(1024)
				#text += b'\r\n'
				length = length - 1024
			put_method(connectionSocket, text)
		elif (words[0] == 'POST'):
			length = int(length)
			length = length - 1024
			while (length > 0):
				text += connectionSocket.recv(1024)
				#text += b'\r\n'
				length = length - 1024
			temp_post_method(connectionSocket, text)
		else:
			default_method(connectionSocket, text)
	except Exception as e:
		print(e)
	connectionSocket.close()


def main():
	global max_users
	max_user = max_users['maxusers']
	max_user = int(max_user)
	while True:
		connectionSocket, addr = serverSocket.accept()
        	#print('ConnectionSocket = ' + str(connectionSocket) + ' ADDR = ' + str(addr))
		if (len(client_list) <= max_user):
			client_list.append(connectionSocket) 
			new_thread = threading.Thread(target=new_receive, args= (connectionSocket,))
			new_thread.start()

try:
	config_object = configparser.ConfigParser()
	config_object.read('gaurav.conf')
	userinfo = config_object["USERINFO"]
	error_log = config_object["ERRORLOG"]
	access_log = config_object["ACCESSLOG"]
	documentRoot = config_object["DOCUMENTROOT"]
	serverroot = config_object["SERVERROOT"]
	max_users = config_object["MAXUSERS"]
	port_number = config_object["PORTNUM"]
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverPort = int(port_number['port_number'])
	serverSocket.bind(('', serverPort))
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.listen()
	print('The Server is ready to receive...')
	main()
except KeyboardInterrupt:
	print("Closing the server....")
	serverSocket.close()
	print("Server Closed")
	
