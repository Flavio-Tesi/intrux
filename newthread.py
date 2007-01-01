import ablib
import time
import db_query

connector_leds="D11"

led = [
	ablib.Daisy11(connector_leds,'L1'),
	ablib.Daisy11(connector_leds,'L2'),
	ablib.Daisy11(connector_leds,'L3'),
	ablib.Daisy11(connector_leds,'L4'),
	ablib.Daisy11(connector_leds,'L5'),
	ablib.Daisy11(connector_leds,'L6'),
	ablib.Daisy11(connector_leds,'L7'),
	ablib.Daisy11(connector_leds,'L8'),
]

x = db_query.read_lights()
lights = []

for i in x:
	if i[2]==0:
		lights.append (True)
	else:
		lights.append (False)

for i in range (0, len(lights)):
	if lights[i] == True:
		led[i].off()
	else:
		led[i].on()		

def rising1(i):
	if lights[i]:
		led[i].on()
		lights[i] = False
		db_query.change_light(i+1)
	else:
		led[i].off()
		lights[i] = True
		db_query.change_light(i+1)

def rising2():
	if lights[3]:
		for i in range (0,10):
			led[5].on()
			time.sleep(0.2)
			led[5].off()
			time.sleep(0.2)
		led[4].on()
		led[6].on()
