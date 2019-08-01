#In order for code to work: The senders email account settings need to allow for "Less secure apps to access"
#uses googles mailing server

from socket import *
import ssl, base64, getpass

client = socket(AF_INET,SOCK_STREAM)	#creating socket with TCP
socket = ssl.wrap_socket(client,ssl_version=ssl.PROTOCOL_TLSv1)
socket.connect(('smtp.gmail.com', 465)) # connecting to server

recv = socket.recv(1024)
print ("recv: %s" % recv)
if (recv[:3] != '220'):		# used mainly for troubleshooting (from github)
    print ('Error 220 reply not received from server.')


helo = 'HELO google\r\n'
socket.send(helo.encode()) # Send HELO command to begin communication with google server
recv1 = socket.recv(1024).decode()
print("recv1: %s" % recv1)
if (recv1[:3] != '250'):
    print('Error 250 reply not received from server.')


user=input("Insert Username: ")
passw=getpass.getpass(prompt='Insert Password: ')

string=str(base64.b64encode(("\000"+user+"\000"+ passw).encode())) # encrypting password
string=string.strip("\n")
string=string[2:len(string)-1]
string = 'AUTH PLAIN '+ string + '\r\n' 	#formatting details to send through
socket.send(string.encode()) #sending through
recv1 = socket.recv(1024)
print(recv1.decode())


# Send MAIL FROM command and print server response.
fromC = 'MAIL FROM: <'+ user+'>\r\n'
print(fromC)
socket.send(fromC.encode())	#sending through socket
recv1 = socket.recv(1024).decode()
print("recv2: %s" % recv1)
if(recv1[:3] != '250'):
    print('Error recv2 to 250 reply not received from server.\n')

# Send RCPT TO command and print server response.
receiver =input("Send email to: ")
toC = 'RCPT TO: <'+ receiver +'>\r\n'
print(toC)
socket.send(toC.encode())	# sending through socket
recv1 = socket.recv(1024).decode()
print("recv3: %s" % recv1)
if (recv1[:3] != '250'):
    print('Error recv3 to 250 reply not received from server.')

# Send DATA command and print server response.
data = 'DATA\r\n'
socket.send(data.encode())
recv1 = socket.recv(1024).decode()
print(recv1)
Subject=input("Subject: ")
Text=input("Message: ")
socket.send(("Subject: "+Subject+"\r\n\r\n"+Text+"\r\n\r\n.\r\n\r\n").encode())
recv1 = socket.recv(1024).decode()
print(recv1)

#Sending quit command and response to show end of transaction
socket.send("QUIT\r\n".encode())
recv1 = socket.recv(1024).decode()
print(recv1)
socket.close()