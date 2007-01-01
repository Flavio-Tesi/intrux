import ablib
import time
import newthread

connector_buttons="D12"
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


for i in range (0,4):
	button[i].set_edge("rising", newthread.rising1)
for i in range (5,8):
	button[i].set_edge("rising", newthread.rising2)

while True: 
	time.sleep(0.1)
