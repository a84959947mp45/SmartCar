# coding=UTF-8
import socket
import sys
import cv2
import numpy as np
from _thread import *
import threading
import random
from pynput.keyboard import Key, Listener
import time 


class Server(threading.Thread):

	def __init__(self,IP,port):
		threading.Thread.__init__(self)
		self.IP = IP
		self.port=port
		self.list_of_clients = []
		self.opened = True
		self.ans=b'N'
		self.KeyBoardHandler=threading.Thread(target=self.ServerStop,args=())
		self.KeyBoardHandler.start()
		self.picture=cv2.imread("output.jpg")
		self.run()
		#self.forever()
		
	def recvall(self,sock, count):
		buf = b''
		while count:
			newbuf = sock.recv(count)
			if not newbuf: return None
			buf += newbuf
			count -= len(newbuf)
		return buf
	def tempSend(self,conn,addr):
		conn.send(self.picture)
		print(len(self.picture))
		conn.close()
	def clientSend(self,conn,addr):#送到手機的
		count=0
		
		conn.send(self.ans)#先送方向
		sendp=True
		while True:
			#print(count)
			try:
				b=conn.recv(2)#接收ok
				#print(b,len(b))
				if b and len(b)>0:#表示未斷線
					#if sendp:
					conn.send(self.ans)#再送圖片
						#sendp=False
						#print('sendp')
					#else:
						#conn.send(self.ans)
						#sendp=True
						#print(self.picture)
					#print(self.ans+self.picture)
				else:
					print("對方離線")
					self.remove(conn,'phone')
					break
			except TimeoutError:
				print("對方已經離開")
				self.remove(conn,'phone')
				break
			except ConnectionResetError: 
				#conn.close()
				print("對方離線")
				self.remove(conn,'phone')
				break
		#conn.send(b'Left')
		conn.close()
		
	def CameraReceive(self,conn,addr):

		count=0
		while count<1000:
			#print(count)
			msg=self.recvall(conn,1)#收方向訊息
			if msg:
				#print(msg)
				self.ans=msg
				length = self.recvall(conn,16)
				if length:
					#print(length)
					stringData = self.recvall(conn, int(length))#圖片資料
					
					data=np.fromstring(stringData, dtype='uint8')#轉成np
					img=cv2.imdecode(data,1)#轉成
					self.picture = img
					cv2.imshow('image',img)
					cv2.waitKey(30)
				
				#conn.send(b'ok')
			else:
				self.remove(conn,'camera')
				conn.close()
				break
		
	def remove(self,connection,id):   
		if connection in self.list_of_clients:
			self.list_of_clients.remove(connection)
		if id=='camera':
			self.opened=0
			self.KeyBoardHandler.join()
			self.server.close()
	def run(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.IP, self.port))
		self.server.listen(100)
		first=True
		while self.opened:
			print ("目前連線人數:",len(self.list_of_clients))
			try:
				conn, addr = self.server.accept()
				self.list_of_clients.append(conn)
				print (conn)
				print ("client's ID: ", addr[1] ," connected")
				
				if first:#接收攝影機資訊
					first=False
					start_new_thread(self.CameraReceive,(conn,addr))
					start_new_thread(self.saveImg,())
				else:#接收手機的通訊
					start_new_thread(self.clientSend,(conn,addr))
					
			except OSError:#按下esc中斷
				print ("強制中斷")
				
				#break
			
			
	def ServerStop(self):
		with Listener(on_press=self.forceStopServer) as listener:#監聽按鍵
			listener.join()
	def forceStopServer(self,key):
		if key == Key.esc:#Stop listener
			self.opened=False
			#creates a temporary socket object, where AF_INET and SOCK_STREAM is the address family and socket type. 
			#This is used to create a connection to the process that is waiting for a connection, so that it can be told to stop waiting! 
			#socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect( (self.IP, self.port))
			self.server.close()
			return False
	def saveImg(self):
		while self.opened:
			time.sleep(0.05)
			cv2.imwrite("output.jpg",self.picture) 
			
A=Server("0.0.0.0",8888)
#A.run()
#A.run()