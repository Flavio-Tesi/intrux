import os
import datetime

#-f pics -d 1000

def on_cam_640_480():
	os.chdir("/root/mjpg-streamer/")
	a = os.popen("./mjpg_streamer -i \"./input_uvc.so -f 10 -r 640x480\" -o \"./output_http.so -w ./www -p 8181\" -o \"./output_file.so \"", "r")
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")
	
def on_cam_1280_720():
	os.chdir("/root/mjpg-streamer/")
	a = os.popen("./mjpg_streamer -i \"./input_uvc.so -f 10 -r 1280x720\" -o \"./output_http.so -w ./www -p 8181\" -o \"./output_file.so\"", "r")
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")

def off_cam():
	a = os.popen("pkill -f \"./mjpg_streamer\"", "r")
	b = a.read()
	a.close()
	
def on_record():
	x = datetime.datetime.now()
	testo = "avconv -an -f video4linux2 -s 320x240  -r 15 -i /dev/video0 -f mp4 /var/www/video/"
	testo+= str(x)[0:10]+"_"+(str(x)[11:19])
	testo+=".mp4"
	a = os.popen(testo, "r")
	b = a.read()
	a.close()
	
def off_record():
	a = os.popen("pkill -f \"avconv\"", "r")
	b = a.read()
	a.close()
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

def leggi_temperatura():
	f = open('/sys/bus/w1/devices/28-000003dcbf67/w1_slave')
	line = f.readline()
	line = f.readline()
	f.close()
	return line[29:31]



"""


def images2video():
	os.chdir("/root/mjpg-streamer/")
	path="pics"
	dirList=os.listdir(path)
	orderedDirList=sorted(dirList)
	i=0
	for fname in orderedDirList:
		previous_name = path + "/" + fname
		new_name = path + "/%03d.jpg" % i
		os.rename(previous_name,new_name) 
		i+=1
	x = str(datetime.datetime.now())[0:10]+"_"+(str(datetime.datetime.now())[11:19])
	testo = "ffmpeg -r 15 -b 200k -i pics/%03d.jpg "
	testo+= x
	testo+= ".mp4"
	a = os.popen(testo, "r")
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")
	a = os.popen("rm /root/mjpg-streamer/pics/*.jpg", "r")
	b = a.read()
	a.close()
	

def leggi_directory_video():
	a = os.popen("ls -la | grep '^d'", "r")
	b = a.read()
	a.close()
	return b



./mjpg_streamer -i "./input_uvc.so -f 10 -r 1280x720" -o "./output_http.so -w ./www -p 8181" -o "./output_file.so" &

wget http://192.168.1.104:8181/stream_simple.html /var/www/video/ciaoooo.mp4

avconv -an -f video4linux2 -s 320x240  -r 15 -i rtp://192.168.1.104:8181/stream_simple.html -f mp4 /var/www/video/ciaooooo.mp4

avconv -an -f video4linux2 -s 320x240  -r 15 -i /dev/video0 -f mp4 -async 1 tcp://192.168.1.104:8181

avconv -f video4linux2 -i /dev/video0 -vcodec mpeg2video -pix_fmt yuv420p -me_method epzs -async 1 http://localhost:8090/stream.mpg

avconv -f video4linux2 -i /dev/video0 -vcodec mpeg2video -r 25 -pix_fmt yuv420p -me_method epzs -b 2600k -bt 256k -f webm http://127.0.0.1:8090/feed1.ffm

ffmpeg -f video4linux2 -i /dev/video0 -s 320x240 -r 25 http://localhost:8090/feed1.ffm

avconv -f video4linux2 -i /dev/video0 udp://localhost:8090/feed1.ffm

avconv -f /etc/ffserver.conf
avconv -v 2 -r 5 -s 640x480 -f video4linux2 -i /dev/video0 ://localhost:8090/webcam.ffm

ffmpeg -f video4linux2 -i /dev/video0 -s 640x480 -r 15 -vcodec mpeg2video -an ://localhost:8090/feed1.ffm

avconv -f video4linux2 -s 320x240 -r 16 -i /dev/video0 -b 128k -vcodec libvpx -vb 448k -f webm http://b.stream.mayfirst.org:8080/publish/mfpl?password=SECRET

avconv -f video4linux2 -i /dev/video0 -vcodec mpeg2video -r 25 -pix_fmt yuv420p -me_method epzs -b 2600k -bt 256k -f rtp rtp://localhost:8090




"""
