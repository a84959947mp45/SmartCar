#! -*- coding:utf-8 -*-
import numpy as np
import cv2
import darknet_AB as dn
import time
import os
import re
import serial
import math
import socket
import sys
from _thread import *

IP = "172.20.10.2"
port=8888
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((IP,port))

global ptn
ptn = bytes("STOP     Z", encoding = "utf8")


count = 1
timefps = 1
net = dn.load_net(str.encode("/home/nvidia/darknet_AB/cfg/yolov3-tiny_peppapig.cfg"),str.encode("/home/nvidia/darknet_AB/yolov3-tiny_peppapig_final.weights"), 0)
meta = dn.load_meta(str.encode("/home/nvidia/darknet_AB/cfg/voc_peppapig.data"))

font = cv2.FONT_HERSHEY_SIMPLEX
line = cv2.LINE_AA
cls_name = "Peppa pig"
BBOX_COLOR = (0,255,0)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
global input_width
global input_height
input_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
input_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


def consol():
    ser = serial.Serial("/dev/ttyTHS2",9600,timeout = 0.5)
    ary = bytearray(ptn)
    ser.write(ary)
    #time.sleep(0.01)
    ser.close
    

def area1():
	x1a = math.floor(r[0][2][0]-r[0][2][2]/2)
	y1a = math.floor(r[0][2][1]-r[0][2][3]/2)
	x1b = math.floor(r[0][2][0]+r[0][2][2]/2)
	y1b = math.floor(r[0][2][1]+r[0][2][3]/2)
	pic_x1 = x1b - x1a
	pic_y1 = y1b - y1a
	global aarea1
	global position1
	aarea1 = pic_x1 * pic_y1
	position1 = (input_width - x1b) - x1a
	print(aarea1)
	#print(x1a,x1b,position1,pic_x1)
	

def detection():
	msg=b'N'
	rgx="[A-Za-z]+"
	file = "/home/nvidia/darknet_AB/out/" + str(int(1)) + ".jpg"
	global r
	r = dn.detect(net, meta, str.encode(file))
	global ptn
	if len(r) == 0 :
		ptn = bytes("STOP     Z", encoding = "utf8")
		print("偵測不到 停止")
		return msg
	else :
		print("偵測到佩佩豬")
		area1()
		if aarea1 > 300000 :
			ptn = bytes("STOP     Z", encoding = "utf8")
			print("距離過近 停止")
		elif -100 <= position1 <= 100 :
			ptn = bytes("GO       Z", encoding = "utf8")
			print("前進")
			msg=b'F'
		elif position1 < -100 :
			ptn = bytes("RIGHT    Z", encoding = "utf8")
			print("右轉")
			msg=b'R'
		elif position1 > 100 :
			ptn = bytes("LEFT     Z", encoding = "utf8")
			print("左轉")
			msg=b'L'
	
	consol()				
	for i in range(len(r)):				
		rx1 = r[i][2][0]-r[i][2][2]/2
		ry1 = r[i][2][1]-r[i][2][3]/2
		rx2 = r[i][2][0]+r[i][2][2]/2
		ry2 = r[i][2][1]+r[i][2][3]/2
		pic_rx = rx2 - rx1
		pic_ry = ry2 - ry1
		frame_rec = cv2.rectangle(frame,(int(rx1),int(ry1)),(int(rx2),int(ry2)),(0,255,0),3)
		txt = '{} {:.2f}'.format(cls_name,r[0][1])
		txt_loc = (int(rx1),int(ry1)-15)
		cv2.putText(frame,txt,txt_loc,cv2.FONT_HERSHEY_TRIPLEX,0.7,BBOX_COLOR,2,cv2.LINE_AA)
		#cv2.imwrite("/home/nvidia/darknet_AB/out/" + str(int(1)) + ".jpg", frame_rec)	
	return msg

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
while(True):
	tic = time.time()
	#consol()
	ret , frame = cap.read()
	if (count % timefps == 0):
		#cv2.imwrite("/home/nvidia/darknet/imgggg/" + str(int(1)) + ".jpg",frame)
		cv2.imwrite("/home/nvidia/darknet_AB/out/" + str(int(1)) + ".jpg",frame)
		msg=detection()
		

		
		#consol()

		toc = time.time()
		fps = 1.0/(toc - tic)
		fps_text = 'FPS: {:.1f}'.format(fps)
		cv2.putText(frame, fps_text, (11, 50), font, 1.0, (0, 255, 255), 4, line)
		#frame_hi=cv2.imread("/home/nvidia/darknet_AB/out/" + str(int(1)) + ".jpg")
		cv2.imshow('frame_rec', frame)
		
				#cv2.resize(image,(32,32)
		#print(frame.shape[0])
		#將圖片轉成封包
		sendframe = cv2.resize(frame,(int(frame.shape[1]*0.2),int(frame.shape[0]*0.2)))
		result, imgencode = cv2.imencode(".jpg", sendframe, encode_param)
		stringData = np.array(imgencode)
		#img=cv2.imread)
		print(msg)
		server.send(msg)
		server.send(str.encode(str(len(stringData)).ljust(16)));
		server.send(stringData );
		#x=server.recv(512)
		
	count = count+1
	if cv2.waitKey(1) &0xFF == ord('q'):
		break

#when everything done , release the capture
cap.release()
cv2.destroyAllWindows()
