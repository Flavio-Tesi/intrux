import ablib
import time

connector_buttons="D12"
connector_leds="D11"

button = [
	ablib.Daisy5(connector_buttons,'P1'),
	ablib.Daisy5(connector_buttons,'P2'),
	ablib.Daisy5(connector_buttons,'P3'),
	ablib.Daisy5(connector_buttons,'P4'),
	ablib.Daisy5(connector_buttons,'P5'),
	ablib.Daisy5(connector_buttons,'P6'),
	ablib.Daisy5(connector_buttons,'P7'),
	ablib.Daisy5(connector_buttons,'P8'),
]

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

x = [True, True, True, True, True, True, True, True]

def P0_rising():
	if x[0]:
		led[0].on()
		x[0] = False
	else:
		led[0].off()
		x[0] = True

def P1_rising():
	if x[1]:
		led[1].on()
		x[1] = False
	else:
		led[1].off()
		x[1] = True

def P2_rising():
	if x[2]:
		led[2].on()
		x[2] = False
	else:
		led[2].off()
		x[2] = True

def P3_rising():
	if x[3]:
		led[3].on()
		x[3] = False
	else:
		led[3].off()
		x[3] = True

def P4_rising():
	if x[4]:
		for i in range (0,10):
			led[5].on()
			time.sleep(0.2)
			led[5].off()
			time.sleep(0.2)
		led[4].on()
		led[6].on()
		


button[0].set_edge("rising", P0_rising)
button[1].set_edge("rising", P1_rising)
button[2].set_edge("rising", P2_rising)
button[3].set_edge("rising", P3_rising)
button[4].set_edge("rising", P4_rising)
button[5].set_edge("rising", P4_rising)
button[6].set_edge("rising", P4_rising)
button[7].set_edge("rising", P4_rising)



while True: 

	time.sleep(0.1)
