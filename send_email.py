import smtplib  
  
fromaddr = 'emailintrusione@gmail.com'  
toaddrs  = '091Ryuk132@gmail.com'  
username = 'emailintrusione@gmail.com'  
password = 'anti-intrusione'  
  
def invia_email_rfid_utente():
	server = smtplib.SMTP('smtp.gmail.com',587)  
	server.starttls()  
	server.login(username,password) 
	msg = "un utente diverso dall'amministratore ha disattivato l'allarme tramite rfid." + "\n" 
	msg+= "per controllare le luci: 192.168.1.104/adminmobile.html#luci" + "\n"
	msg+= "per riattivare l'allarme: 192.168.1.104/adminmobile.html#intrusioni" + "\n"
	msg+= "per visualizzare la videocamera: 192.168.1.104/adminmobile.html#realtime" + "\n"
	server.sendmail(fromaddr, toaddrs, msg)  
	server.quit()  

def invia_email_intrusione():
	server = smtplib.SMTP('smtp.gmail.com',587)  
	server.starttls()  
	server.login(username,password) 
	msg = "ATTENZIONE!! E' STATO ATTIVATO L'ALLARME!!" + "\n" + "guarda: 192.168.1.104/adminmobile.html#realtime" 
	server.sendmail(fromaddr, toaddrs, msg)  
	server.quit()  
