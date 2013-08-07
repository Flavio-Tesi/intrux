import os
import datetime

def on_cam_640_480():
	os.chdir("/root/mjpg-streamer/")
	a = os.popen("./mjpg_streamer -i \"./input_uvc.so -f 10 -r 640x480\" -o \"./output_http.so -w ./www\" -o \"./output_file.so -f pics -d 1000\"", "r")
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")
	
def on_cam_1280_720():
	os.chdir("/root/mjpg-streamer/")
	a = os.popen("./mjpg_streamer -i \"./input_uvc.so -f 10 -r 1280x720\" -o \"./output_http.so -w ./www\" -o \"./output_file.so -f pics -d 1000\"", "r")
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")

def off_cam():
	a = os.popen("pkill -f \"./mjpg_streamer\"", "r")
	b = a.read()
	a.close()
	
def on_record():
	testo = "avconv -an -f video4linux2 -s 320x240  -r 15 -i /dev/video0 -vcodec mpeg4 -vtag DIVX /var/www/video/"
	testo+= str(datetime.datetime.now())[0:10]+"_"+(str(datetime.datetime.now())[11:19])
	testo+=".avi"
	a = os.popen(testo, "r")
	b = a.read()
	a.close()

"""
def compact_image():
	os.chdir("/root/m/")
	testo = "avconv -i "
	testo+= x
	testo+=".avi "
	testo+= x
	testo+=".mp4"
	a = os.popen(testo, "r")
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")
	testo = "rm /var/www/video/"
	testo+= x
	testo+=".avi"
	a = os.popen(testo, "r")
	b = a.read()
	a.close()
	"""
	
def off_record():
	a = os.popen("pkill -f \"avconv\"", "r")
	b = a.read()
	a.close()
		 
def on_hotspot():
	os.chdir("/root/")
	a = os.popen("hostapd hostapd.conf &", "r")
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")
	
def off_hotspot():
	a = os.popen("pkill -f \"hostapd hostapd.conf\"", "r")
	b = a.read()
	a.close()

def leggi_directory_video():
	a = os.popen("ls -la | grep '^d'", "r")
	b = a.read()
	a.close()
	return b
	
	
	
	

