import serial
 
ser2 = serial.Serial(
    port='/dev/ttyS4', 
    baudrate=9600, 
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)    


def goto_form (index):
	
	lista = ["\x01","\x0A",chr(index),"\x00","\x00"]
	ls1 = lista[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser2.write(lista[i])

def string_write (index, numero_codice):
	
	lista = ['\x02', chr(index), '\x01',chr(ord(numero_codice))]
	ls1 = ls_ser[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser2.write(ls_ser[i])
		
def light_led (index, bit):
	lista = ["\x01","\x0E",chr(index),"\x00",chr(bit)]
	ls1 = lista[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser2.write(lista[i])
	
def set_temperature (index, val):
	lista = ["\x01","\x12",chr(index),"\x00",chr(val)]
	ls1 = lista[0]	
	for i in range (1, len(lista)):
		ls1 = calcola_checksum(ls1, lista[i])
	lista.append(ls1)
	for i in range (0, len(lista)):
		ser2.write(lista[i])

def calcola_checksum (comando, parametro):
	com = ord(comando)
	for i in range (0, len(parametro)):
		com = com ^ ord(parametro[i])
	com = chr(com)
	return com
	
def verifica (lista):
	if len(lista) == 6:
		pwd1 = "170509"
		pwd2 = "905071"
		lista_control1 = []
		for i in range (0, len(pwd1)):
			lista_control1.append(pwd1[i])
		lista_control2 = []
		for i in range (0, len(pwd2)):
			lista_control2.append(pwd2[i])
			
		if lista == lista_control1:
			del lista[0:6]
			return 1
							
		elif lista == lista_control2:		
			del lista[0:6]
			return 2
								
	else:
		del lista[0:99]
		return 3
		
def spacchetta(pacchetto):
	comando = pacchetto[0]
	parametro = pacchetto[1:-1]
	checksum = pacchetto[-1]
	chk = calcola_checksum (comando, parametro)		
	if chk == checksum:
		return "OK"
	else:
		return "NO"
	
def function(): 
	lettura = ser2.read(1) 
	if len(lettura)>0:	
#		print "%x" %(ord(lettura))
		return lettura
		
"""		
	else:
		if len(pacchetto)>=3:
			spacchettamento = spacchetta(pacchetto)
			if spacchettamento == "OK":
				numero_codice = pacchetto[-2]
				numero_bottone = pacchetto [2]
				comando = pacchetto [1]
				if numero_codice == "\x08":
					x = verifica(lista)
					return x
				elif numero_codice == "\x3c":
					if len(lista)>0:
						for i in range (0, len(lista)):
							print lista[i]
						del lista [-1]
				elif (comando == "\x06") & (numero_bottone == "\x00"):
					return "attiva_allarme"
				elif (comando == "\x06") & (numero_bottone == "\x01"):
					goto_form(1)
				elif (comando == "\x06") & (numero_bottone == "\x02"):
					return "attiva_allarme"
					
				else:
					lista.append (numero_codice)
		pacchetto = ""
	
"""
