import RPi.GPIO as GPIO
import time
import sys
import tty
import threading
import serial
import time

#ser = serial.Serial("/dev/ttyUSB0", 9600)

def origin():
        LED_PIN =31
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LED_PIN, GPIO.OUT)
        p2 = GPIO.PWM(LED_PIN, 63)
        p2.start(9)
        
        time.sleep(0.5)

        p2.stop()
        GPIO.cleanup()

def right():
        LED_PIN =31
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LED_PIN, GPIO.OUT)
        p2 = GPIO.PWM(LED_PIN, 63)
        p2.start(9)

        try:
			for dc in range(9, 6, -1):
				p2.ChangeDutyCycle(dc)
				time.sleep(0.2)
        except:
            pass
        p2.stop()
        GPIO.cleanup()

def left():
        LED_PIN =31
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LED_PIN, GPIO.OUT)
        p2 = GPIO.PWM(LED_PIN, 63)
        p2.start(9)
        try:
                for dc in range(9, 12, 1):
                    p2.ChangeDutyCycle(dc)
                    time.sleep(0.2)

        except:
            pass
        p2.stop()
        GPIO.cleanup()

def go():
    LED_PIN =16

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    p2 = GPIO.PWM(LED_PIN, 63)
    p2.start(10.5)
    time.sleep(0.3)
    p2.stop()
    GPIO.cleanup()

def main():

	ser = serial.Serial("/dev/ttyUSB0", 9600)
	while True:
		str=" "
		 # 獲得接收緩衝區內容
		count = ser.inWaiting()
		if count != 0:
			# 讀取內容，並編碼
			recv = ser.read(count)
			str=recv.decode("utf-8") 
		
			ser.write(recv)
		# 清空接收緩衝區
		ser.flushInput()
	    #打訊號給車子
		process(str[0])



def process(key):
    if key!=" ":
        print(key)
    if key == 'x':
       exit('exitting')
    elif key == 'G':
       print(key, end="", flush=True)
       origin()
       go()
	   
    elif key == 'S':
       print(key, end="", flush=True)
       origin()
	   
       
    elif key == 'R':
       print(key, end="", flush=True)
       right()
       go()
	   
    elif key == 'L':
       print(key, end="", flush=True)
       left()
       go()


def default():
  LED_PIN =16

  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(LED_PIN, GPIO.OUT)
  p1 = GPIO.PWM(LED_PIN, 63)
  p1.start(6)
#  right()
  try:
      while True:
          for dc in range(6, 11, 1):
                        p1.ChangeDutyCycle(dc)
                        time.sleep(0.1)
          for dc in range(11, 6, -1):
                      p1.ChangeDutyCycle(dc)
                      time.sleep(0.1)
     # go()
  except:
     pass

  p1.stop()
  GPIO.cleanup()
 

if __name__ == "__main__":
    try:
        main()
        #default()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()



