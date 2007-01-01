import os

def on_cam_640_480():
	os.chdir("/root/mjpg-streamer/")
	a = os.popen("./mjpg_streamer -i \"./input_uvc.so -f 15 -r 640x480\" -o \"./output_http.so -w ./www\"", "r")
	print "ciaoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")
	
def on_cam_1280_720():
	os.chdir("/root/mjpg-streamer/")
	a = os.popen("./mjpg_streamer -i \"./input_uvc.so -f 15 -r 1280x720\" -o \"./output_http.so -w ./www\"", "r")
	print "ciaoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
	os.chdir("/root/intrux/")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")


def off_cam():
	a = os.popen("pkill -f \"./mjpg_streamer\"", "r")
	b = a.read()
	a.close()
	 
def on_hotspot():
	os.chdir("/root/")
	a = os.popen("hostapd hostapd.conf &", "r")
	b = a.read()
	a.close()
	os.chdir("/root/intrux/")
	
def off_hotspot():
	a = os.popen("pkill -f \"hostapd hostapd.conf\"", "r")
	b = a.read()
	a.close()
