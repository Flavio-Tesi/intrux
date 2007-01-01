import ablib
import time
import daisy_function

conn12 = 'D12'
out0 = 'RL0'
out1 = 'RL1'
pos1 = 'first'
pos2 = 'second'

sirena =				ablib.Daisy8(connector=conn12,id=out0,position=pos1)
lampeggiante = 			ablib.Daisy8(connector=conn12,id=out1,position=pos1)
luceAllarmeAvvenuto =	ablib.Daisy8(connector=conn12,id=out0,position=pos2)



for i in range (0,10):
	lampeggiante.on()
	time.sleep(0.5)
	lampeggiante.off()
	time.sleep(0.5)
sirena.on()
luceAllarmeAvvenuto.on()
