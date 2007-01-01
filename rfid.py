import serial
 
ser = serial.Serial(
    port='/dev/ttyS2', 
    baudrate=9600, 
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)  

def controlla(codice):
	if codice == [48,49,48,55,52,67,53,68,51,48,50,55] or codice == [48,49,48,55,52,67,54,53,57,55,66,56]:
		del codice[0:99] 
		return True
	del codice[0:99]







codice = []

def function():
	s = ser.read(1)
	if (len(s)>0 and ord(s)!=0x02 and ord(s)!=0x03 and ord(s)!=0x0D and ord(s)!=0x0A):	
		codice.append (ord(s))
	if len(codice)==12:
		return controlla(codice)
