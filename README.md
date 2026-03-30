M01 Assignment - RBAC and Authenitication Mini App
  This application provides confidentiality because it searches through the users currently on file and only allows access into the admin endpoint or the user endpoint if the password credentials entered match the case. It also assesses what role has
  been given to each specific user and this determines which endpoint to connect to. The way that the code is set up, you should not be able to gain access to the admin panel or user panel if you first don't match the credentials on file. Then you you with
  be subject to authorization which in turn opens the correct endpoint for you. If you are not in the system, a generic error message is politely prompted. 
  
  In a sense there is integrity because the app doesn't allow for any input of data on the separate endpoints, haha. Integrity is the trustworthiness of the information. The goal is to prevent a bad actor from having the ability to manipulate your data or to 
  delete it altogether. 
  
  Availability ensures that the information is safe from threats like DDOS which overloads a service until it crashes. 
  
  The objective is to remember these three concepts when securing an application and to concern oneself with them at every step of the process. I believe that the more often you consider these conditions, you not only lessen the likelihood of leaving a hack
  to be discovered, but you may also discover a more secure method for the future. 
  
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
M02 Assignment - Encryption and Decryption Demo
  I decided to stem off of the RBAC and Authentication Mini App that I created the week before. I want to develop some confidence with tkinter before moving on to other GUI building frameworks. This week I moved all of the logic into a LoginApp() class to make       variable calls more easy (until I started nesting my methods xD). I added methods that allowed me to use the admin panel to create a client and a server using the socket library. I used the tcp protocol (SOCK_STREAM). I also installed the cryptography library to   use Fernet for symmetric key encryption and hazmat for asymmetric encryption. This has been made available with a pip install -r requirements.txt. 

  The order that the windows needs to be open is critical:
    - First log into admin.
    - Then click open server.
    - Then open login
    - Now log in again but as a user
    - Click the fire me button
    - Now you can open the client server and start chatting.

  A button command allows me to use an open_server() method and open_client() method from the admin window. The client and the server have a very similar interface appearance, but I created a second class called SecureMessage() to handle the network and              encryption. The open_server and open_client methods instantiate their own SecureMessage() object (self.server_network = SecureMessage() and self.client_network = SecureMessage()). Concurrency was needed because both tkinter mainloop() and socket methods require    continuous listening (looping) and the GUI will freeze up. threading was used to solve this issue. 

  Once I was able to get the messages to send and receive after adding the encryption logic, I defined a method that creates another window (def open_sniffer()) and attached it to another button, but this time in the user window ('Fire Me'). It basically creates a   scolling text box that outputs the traffic that passes between the interceptor and the server/client (server <--> interceptor <--> client). This proves that the data is encrypted between the output you see in the client and server message control message log.
