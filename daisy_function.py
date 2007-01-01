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

def P0_rising():
	if lights[0]:
		led[0].on()
		lights[0] = False
		db_query.change_light(1)
	else:
		led[0].off()
		lights[0] = True
		db_query.change_light(1)

def P1_rising():
	if lights[1]:
		led[1].on()
		lights[1] = False
		db_query.change_light(2)
	else:
		led[1].off()
		lights[1] = True
		db_query.change_light(2)

def P2_rising():
	if lights[2]:
		led[2].on()
		lights[2] = False
		db_query.change_light(3)
	else:
		led[2].off()
		lights[2] = True
		db_query.change_light(3)

def P3_rising():
	if lights[3]:
		led[3].on()
		lights[3] = False
		db_query.change_light(4)
	else:
		led[3].off()
		lights[3] = True
		db_query.change_light(4)

def P4_rising():
	if lights[4]:
		for i in range (0,10):
			led[5].on()
			time.sleep(0.2)
			led[5].off()
			time.sleep(0.2)
		led[4].on()
		led[6].on()


funzioni = [P0_rising, P1_rising, P2_rising, P3_rising, P4_rising]
