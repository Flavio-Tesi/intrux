import serial
import lib_screen
 
ser = serial.Serial(
    port='/dev/ttyS4', 
    baudrate=9600, 
    timeout=0.1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)  

def goto_form (ser, index):
	
	lista = ["\x01","\x0A",chr(index),"\x00","\x00"]
	ls1 = lista[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser.write(lista[i])

def string_write (ser, index, numero_codice):
	
	lista = ['\x02', chr(index), '\x01',chr(ord(numero_codice))]
	ls1 = ls_ser[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser.write(ls_ser[i])
		
def light_led (ser, index, bit):
	lista = ["\x01","\x0E",chr(index),"\x00",chr(bit)]
	ls1 = lista[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser.write(lista[i])
	
def set_temperature (ser, index, val):
	lista = ["\x01","\x12",chr(index),"\x00",chr(val)]
	ls1 = lista[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser.write(lista[i])
pacchetto = ""
lista = []

while True: 
	s = ser.read(1) 
	if len(s)>0:	
		pacchetto="".join([pacchetto,s])
	else:
		if len(pacchetto)>=3:
			s = spacchetta(pacchetto)
			if s == "OK":
				numero_codice = pacchetto[-2]
				if numero_codice == "\x08":
					x = verifica(lista)
					if x == 1:
						goto_form(1)
					elif x == 2:
						goto_form(2)
					elif x == 3:
						goto_form(3)
				elif numero_codice == "\x3c":
					if len(lista)>0:
						for i in range (0, len(lista)):
							print lista[i]
						del lista [-1]
				else:
					lista.append (numero_codice)
					string_write (ser, numero_codice)
		pacchetto = ""
	
ser.close()
