M01 Assignment - RBAC and Authenitication Mini App
  This application provides confidentiality because it searches through the users currently on file and only allows access into the admin endpoint or the user endpoint if the password credentials entered match the case. It also assesses what role has
  been given to each specific user and this determines which endpoint to connect to. The way that the code is set up, you should not be able to gain access to the admin panel or user panel if you first don't match the credentials on file. Then you you with
  be subject to authorization which in turn opens the correct endpoint for you. If you are not in the system, a generic error message is politely prompted. 
  
  In a sense there is integrity because the app doesn't allow for any input of data on the separate endpoints, haha. Integrity is the trustworthiness of the information. The goal is to prevent a bad actor from having the ability to manipulate your data or to 
  delete it altogether. 
  
  Availability ensures that the information is safe from threats like DDOS which overloads a service until it crashes. 
  
  The objective is to remember these three concepts when securing an application and to concern oneself with them at every step of the process. I believe that the more often you consider these conditions, you not only lessen the likelihood of leaving a hack
  to be discovered, but you may also discover a more secure method for the future. 
  
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
  
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
M03 Assignment -  Secure Hashing and Encryption
  For this assignment, I went a little easier on myself and did not incorporate tkinter. I really wanted to get a grasp on the library and the last two assignments helped tremendously. I needed to focus on time effeciency this week so that I can have time to work on the group project in my other class. I used this assignment as an opportunity to strengthen my class comprehension. 
  I have created three classes to handle the three objectives of this assignment. 
    1. Write an app that uses a simple substitution cipher (Caesar cipher or similar) to encrypt/decrypt input text. (CaesarSubstitution())
    2. Write an app that generates SHA-256 hashes for input strings or files. (HashingSHA())
    3. Use OpenSSL or a tool to simulate a digital signature (sign/verify). (Signature())
    
  I placed everything in a while loop so that you could run through each objective without restarting the program.
  - To exit the program type 'quit'.
**CaesarSubstitution()**
  For this class, I controlled the shift in the ASCII code to avoid having additional code to limit the range of input. You are prompted to enter a message and the program runs an encryption and decryption process that results in the output for each process.
  - We are converting the message to ASCII values using ord(char), iterating through the string.
  - I apply a shift value of 10 which is added to the ASCII value. The range is checked to make sure that the values fall between 97-122 (lowercase alphabet)
  - Then the ASCII value is converted to the character representation.
  - The result is appended to a variable called 'result'.

**HashingSHA()**
  This class is designed to initialize by requesting an input to store as the message. I use Python's hashlib library to create a hashed object and a hexidecimal digest for legibility.
  - The hash_encode function stores the orginal hex value and prints it.
  - The modify_msg function stores a modified hex value and prints it, so that you can see that even changing one character modifies the whole hash.
  - The revert_msg function asks that you type the orignal message, so that you can see that the hash values are identical.

**Signature()**
  This class utilizes the cryptography library. In a nutshell what happens is this:
  - private and public keys are generated for both the sender and the rceiver.
  - sender function accepts an input message.
  - sender uses sender_private_key to sign the message.
  - The parameters are the message, the padding and the hashing function used.
  - The padding has additional parameters. The mask generation function spreads randomness across the data. salt_length defines how much random noise to add.
  - The padding is being hashed with SHA256 as well and the salt is added to the message hash.
  - Rceiver function is decrypting the signature to obtain the hashed value of the message received.
  - It also takes the message received and uses the same hashing algorithm.
  - The values are compared to see if they match.
  - A message is displayed with success or failure depending on whether the message was tampered with or not.

  The user has the option to tamper with the message to see that the sign() and verify() methods are working appropriately.
