import smtplib  
  
fromaddr = 'email_mittente@gmail.com'  
toaddrs  = 'email_destinatario@gmail.com'  
username = 'email_mittente@gmail.com'  
password = 'password_email_mittente'  

server = smtplib.SMTP('smtp.gmail.com',587)  
server.starttls()  
server.login(username,password) 
msg = "MESSAGGIO" 
server.sendmail(fromaddr, toaddrs, msg)  
server.quit()  
