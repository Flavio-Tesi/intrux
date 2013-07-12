import sys
sys.path.append('/root/Tesi/mysql')
import db_query

def calcola_checksum (comando, parametro):
	com = ord(comando)
	for i in range (0, len(parametro)):
		com = com ^ ord(parametro[i])
	com = chr(com)
	return com
	
def verifica (lista):
	if len(lista) == 6:
		pwd1 = read_userCode(1)
		pwd2 = read_userCode(2)
		print pwd1
		print pwd2
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
	
