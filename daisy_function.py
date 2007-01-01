import ablib
import time
import db_query
import os

conn11 = 'D11'
conn12 = 'D12'
out0 = 'RL0'
out1 = 'RL1'
in0 = 'IN0'
in1 = 'IN1'
pos1 = 'first'
pos2 = 'second'

luceCamera =			ablib.Daisy8(connector=conn11,id=out0,position=pos1)
luceCameretta =			ablib.Daisy8(connector=conn11,id=out1,position=pos1)
luceCucina =			ablib.Daisy8(connector=conn11,id=out0,position=pos2)
luceSala =				ablib.Daisy8(connector=conn11,id=out1,position=pos2)
sirena =				ablib.Daisy8(connector=conn12,id=out0,position=pos1)
lampeggiante = 			ablib.Daisy8(connector=conn12,id=out1,position=pos1)
luceAllarmeAvvenuto =	ablib.Daisy8(connector=conn12,id=out0,position=pos2)

pulsanteLuceCamera = 	ablib.Daisy8(connector=conn11,id=in0,position=pos1)
pulsanteLuceCameretta = ablib.Daisy8(connector=conn11,id=in1,position=pos1)
pulsanteLuceCucina = 	ablib.Daisy8(connector=conn11,id=in0,position=pos2)
pulsanteLuceSala = 		ablib.Daisy8(connector=conn11,id=in1,position=pos2)
intrusioneCamera =	 	ablib.Daisy8(connector=conn12,id=in0,position=pos1)
intrusioneCameretta = 	ablib.Daisy8(connector=conn12,id=in1,position=pos1)
intrusioneCucina = 		ablib.Daisy8(connector=conn12,id=in0,position=pos2)
intrusioneSala = 		ablib.Daisy8(connector=conn12,id=in1,position=pos2)

x = db_query.read_lights()
lights = []

for i in x:
	if i[2]!=0:
		lights.append (True)
	else:
		lights.append (False)

if lights[0]:
	luceCamera.on()
else:
	luceCamera.off()
if lights[1]:
	luceCameretta.on()
else:
	luceCameretta.off()
if lights[2]:
	luceCucina.on()
else:
	luceCucina.off()
if lights[3]:
	luceSala.on()
else:
	luceSala.off()
	
def lCamera ():
	if lights[0]:
		luceCamera.off()
	else:
		luceCamera.on()
	lights[0] = not(lights[0])
	db_query.change_light(1)
	
def lCameretta ():
	if lights[1]:
		luceCameretta.off()
	else:
		luceCameretta.on()
	lights[1] = not(lights[1])
	db_query.change_light(2)

def lCucina ():
	if lights[2]:
		luceCucina.off()
	else:
		luceCucina.on()
	lights[2] = not(lights[2])
	db_query.change_light(3)

def lSala ():
	if lights[3]:
		luceSala.off()
	else:
		luceSala.on()
	lights[3] = not(lights[3])
	db_query.change_light(4)
	
def alarm ():
	a = os.popen("python allarme.py &", "r")
	b = a.read()
	a.close()

funzioni = [lCamera, lCameretta, lCucina, lSala, alarm]

def stop_allarme ():
	a = os.popen("pkill -f \"python allarme.py\"", "r")
	b = a.read()
	a.close()
	lampeggiante.off()
	sirena.off()
	luceAllarmeAvvenuto.off()
	time.sleep(2)
	db_query.stop_intrusion()

def luci():
	if pulsanteLuceCamera.get():
		lCamera()
	if pulsanteLuceCameretta.get():
		lCameretta()
	if pulsanteLuceCucina.get():
		lCucina()
	if pulsanteLuceSala.get():
		lSala()

def allarme():
	if intrusioneCamera.get():
		alarm()
		db_query.is_intrusion(1)
	if intrusioneCameretta.get():
		alarm()
		db_query.is_intrusion(2)
	if intrusioneCucina.get():
		alarm()
		db_query.is_intrusion(3)
	if intrusioneSala.get():
		alarm()
		db_query.is_intrusion(4)
