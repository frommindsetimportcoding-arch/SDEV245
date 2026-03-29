"""
Creating a basic app that demonstrates the core ideas of authentication, roles and access control.

I think I am going to try to do this using tkinter. I am using tkinter v 8.6.15

UPDATE - I am going to attempt to add an encrypted messaging functionaility between the two applications.
        This may require threading because tkinter continously loops as well as socket methods used to move 
        messages between to applications. 
"""

############ ALL OF THIS BELOW IS NOTES FROM THE PYTHON DOCS. THIS IS MY FIRST TIME REALLY WORKING WITH TKINTER. ########################
############################# PROCEED TO VARIABLE INITIALIZATION #######################################

# Optional variables defined in docs.python.org/3/library/tkinter.html#module-tkinter
# class tkinter.Tk(screen_name=None, base_name=None, class_name='Tk', use_Tk=True, sync=False, use=None) 
# tkinter.Tcl(screen_name=None, base_name=None, class_name='Tk', use_Tk=False)


"""
To find out what configuration options are available on any widget, call its configure() method,
 which returns a dictionary containing a variety of information about each object, including its
default and current values. Use keys() to get just the names of each option.

btn = ttk.Button(frm, ...)
print(btn.configure().keys())


As most widgets have many configuration options in common, it can be useful to find out which are specific to a particular widget class.
Comparing the list of options to that of a simpler widget, like a frame, is one way to do that.

print(set(btn.configure().keys()) - set(frm.configure().keys()))

Similarly, you can find the available methods for a widget object using the standard dir() function. 
If you try it, you’ll see there are over 200 common widget methods, so again identifying those specific to a widget class is helpful.

print(dir(btn))
print(set(dir(btn)) - set(dir(frm)))


"""
# Here is an example from the documentation, for reference. This makes use of from tkinter import *

# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text='Hello World').grid(column=0, row=0)
# ttk.Button(frm, text='Quit', command=root.destroy).grid(column=1, row=1)

# print(ttk.Label.config(frm))
# root.mainloop()

###########################################################################################################
# And here is an example which makes use of import tkinter as tk.

# class App(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.pack()

# # Create the application
# myapp= App()

# #
# # Here are the method calls to the window manager class
# #

# myapp.master.title('My Do-Nothing Application')
# myapp.master.maxsize(1000,400)
################################# Login App #########################################################

from tkinter import *
from tkinter import ttk, scrolledtext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import threading, queue
import socket


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title('User Login')

        # These are the dictionaries that I will use to establish Authentication and Authorization
        self.user_roles = {
            'admin': ['lovelace', 'knuth'],
            'user': ['bob', 'jerry']
        }
        self.credentials = {
            'lovelace': 'ada',
            'knuth': 'donald', 
            'bob': 'bob',
            'jerry': 'jerry'
        }

        # Setting up the user interface. This is done during the initialization of ht LoginApp(root) class.
        self.setup_ui()

    def setup_ui(self):
        """ This builds the main login screen."""
        self.mainframe = ttk.Frame(self.root, padding=(3, 3, 12, 12))
        self.mainframe.grid(column=0, row=0, sticky='NSEW')

        # Variables received from input.
        self.username_var = StringVar()
        self.password_var = StringVar()

        # This will create the entry widgets.
        ttk.Label(self.mainframe, text='Username: ').grid(column=1, row=1, sticky='E')
        self.user_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.username_var)
        self.user_entry.grid(column=2, row=1, sticky='WE')

        ttk.Label(self.mainframe, text='Password: ').grid(column=1, row=2, sticky='E')
        self.pw_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.password_var)
        self.pw_entry.grid(column=2, row=2, sticky='WE')

        # This will create the login button.
        self.login_btn = ttk.Button(self.mainframe, text='Log In', command=self.authenticate)
        self.login_btn.grid(column=3, row=3, sticky='W')

        # Error label will now be persistent but will initialize as an empty string.
        self.error_label = ttk.Label(self.mainframe, text='', foreground='red')
        self.error_label.grid(column=3, row=1, sticky='W')

        # This will configure the layout.
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        # This places the cursor in the user_entry widget and binds the Return key to the same function as the login_btn.
        self.user_entry.focus()
        self.root.bind('<Return>', lambda event: self.authenticate())

    
    def authenticate(self):
        """ Validates the credentials and, if True, begins authorization logic using authorize() function."""
        user = self.username_var.get()
        pw = self.password_var.get()

        if user in self.credentials and self.credentials[user] == pw:
            self.error_label.config(text='')  # This will clear an error label from a previously failed login attempt
            self.authorize(user)
        else:
            self.error_label.config(text='Invalid Username or Password') # An error message will be displayed in 'red' due to previous formatting of the persistent widget.

    
    def authorize(self, user):
        """ This is redirect to a specific window dendent on the privelages established in the user_roles dictionary."""
        if user in self.user_roles['admin']:
            self.open_admin()
        elif user in self.user_roles['user']:
            self.open_user()
    

    def open_admin(self):
        """ Logic to provide unique capabilites for each window. This will handle the logic for those with administrative priveleges. """
        self.root.withdraw()    # Hides the login window

        admin_window = Toplevel(self.root)
        admin_window.title('Administrative Controls')

        # When the 'x' is clicked, a close_panel() function will carry on and bring the login window back.
        admin_window.protocol('WM_DELETE_WINDOW', lambda: self.close_panel(admin_window))

        admin_frame = ttk.Frame(admin_window, padding=20)
        admin_frame.pack(expand=True, fill='both')

        ttk.Label(admin_frame, text='Administrative Message Panel', foreground='purple', font=('Roboto', 12)).pack(pady=10)
        ttk.Button(admin_frame, text='Logout', command=lambda: self.close_panel(admin_window)).pack()
        ttk.Button(admin_frame, text='Open Login', command=lambda: self.open_login()).pack()
        ttk.Button(admin_frame, text='Open Client', command=lambda: self.open_client()).pack()
        ttk.Button(admin_frame, text='Open Server', command=lambda: self.open_server()).pack()
    

    def open_user(self):
        """ Logic prices unique capabilities for the user window. Those who are only granted user priveleges. """
        self.root.withdraw()

        user_window = Toplevel(self.root)
        user_window.title('User Controls')

        user_window.protocol('WM_DELETE_WINDOW', lambda: self.close_panel(user_window))

        user_frame = ttk.Frame(user_window, padding=20)
        user_frame.pack(expand=True, fill='both')

        ttk.Label(user_frame, text="Jerry and Bob's Message Panel", foreground='green', font=('Roboto', 12)).pack(pady=10)
        ttk.Button(user_frame, text='Logout', command=lambda: self.close_panel(user_window)).pack()
        

        def open_sniffer():
            """ Opens a window used to intercept the traffic, proving encryption."""
            sniffer_window = Toplevel(self.root)
            sniffer_window.title('Packet Sniffing the Admin is bad')
            
            sniffer_frame = ttk.Frame(sniffer_window, padding=20)
            sniffer_frame.pack(expand=True, fill='both')

            ttk.Label(sniffer_frame, text='Network Traffic Interceptor', foreground='red', font=('Roboto', 14, 'bold')).pack(pady=5)

            # This will give us a scolling text box showing the intercepted traffic in its encrypted form.
            sniff_log = scrolledtext.ScrolledText(sniffer_frame, width=50, height =20, bg='black', fg='lime')
            sniff_log.pack(padx=5, pady=10)
            sniff_log.insert(END, 'Status: Monitoring Port 6789...\n' + '-'*40 +'\n')

            


            def bridge(source, destination, label):
                while True:
                    try:
                        data = source.recv(4096)
                        if not data: break

                        # Log the encrypted data to the user interface sniffer_window.
                        hex_data = data.hex(' ')
                        self.root.after(0, lambda: sniff_log.insert(END, f'[{label}] {hex_data}\n\n'))
                        self.root.after(0, lambda: sniff_log.see(END))

                        # Forward the data to the endpoint with the encryption key.
                        destination.send(data)
                    except: break
        
            def start_sniffer():
                """ The logic used to intercept the raw data and display the encrypted bytes and then forward the data to the final destination. """
                proxy_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxy_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                proxy_listener.bind(('localhost', 6789))
                proxy_listener.listen(1)

                client_conn, addr = proxy_listener.accept()

                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_sock.connect(('localhost', 6790))


            

                # I will create two threads to handle the bi-dirctional traffic
                threading.Thread(target=bridge, args=(client_conn, server_sock, 'CLIENT->SERVER'), daemon=True).start()               
                threading.Thread(target=bridge, args=(server_sock, client_conn, 'SERVER->CLIENT'), daemon=True).start()

            # It was a horrible idea trying to nest the functions. Function order is important. 
            # Had to throw this down below start_sniffer() so that It could have an object to associate to.
            threading.Thread(target=start_sniffer, daemon=True).start()
        
        # Pretty much the same thing is happening here. Worth revisiting to clean the code.
        ttk.Button(user_frame, text='Fire Me', command=open_sniffer).pack(pady=5)


    def close_panel(self, window):
        """ Destroys the top window and unhides the login screen."""
        window.destroy()
        self.username_var.set('')   # Clears the fields before bringing the login window back.
        self.password_var.set('')
        self.root.deiconify()
        self.user_entry.focus()       # Brings the login screen back.

    
    def open_login(self):
        """ Allows for opening the login window without destroying the current window.
            This is necessary so that I can use the separate windows as a client and 
            server for encrypted messaging."""
        self.username_var.set('')
        self.password_var.set('')
        self.root.deiconify()
        self.user_entry.focus()

    
    def open_client(self):
        """ This window will create a client node that will use select between asymmetric and symmetric encription methods
            It will establish a connection with the server. There will be text entry to send messages to the server and 
            there will be a text box to receive messages from the server."""
        
        # Instantiates a network object.
        self.client_network = SecureMessage()
        

        def handle_send():
            """ Creates msg object which gets data currently in client_message when 'Send' button
                is clicked. Calls on SecureMessage.send_data(msg) to send over the established
                connection."""
            msg = client_message.get('1.0', END).strip()
            if msg:
                self.client_network.send_data(msg)
                message_log.insert(END, f'You: {msg}\n')
                message_log.see(END)
                client_message.delete('1.0', END)


        # Threading will target start_client_node() which will call listen_loop() method to allow a thread to listen in the background
        # for server messages.
        def listen_loop():
            """ This function creates a loop that constantly checks for a message from the server."""
            while True:
                msg = self.client_network.receive_data()
                if msg:
                    # root.after allows us to update the UI from a thread.
                    self.root.after(0, lambda m=msg: message_log.insert(END, f'Server: {m}\n'))


        # I am adding a start_client_node to call the listen_loop() and init_client(). 
        # This should safely run all the mainloop() breaking logic in background threads. 
        def start_client_node():
            self.client_network.init_client()
            self.root.after(0, update_key_label)
            listen_loop()


        def update_key_label():
            """ Helps to refresh the UI with an active key string using the SecureMessage.get_keys_info() method."""
            key_info = self.client_network.get_keys_info()
            self.key_display.config(text=key_info)


        client_window = Toplevel(self.root)
        client_window.title('Client Connection')

        client_frame = ttk.Frame(client_window, padding=20)
        client_frame.pack(expand=True, fill='both')

        ttk.Label(client_frame, text='Message Control', foreground='orange', font=('Roboto', 36)).pack(pady=10)
        ttk.Label(client_frame, text='Compose', foreground='orange', font=('Roboto', 20)).pack(pady=5, side=LEFT)
        ttk.Label(client_frame, text='Message Log', foreground='orange', font=('Roboto', 20)).pack(pady=5, side=RIGHT)
        client_message = Text(client_frame, width=30, height=10, wrap='word')
        client_message.pack(padx=5, pady=10, side=LEFT)
        message_log = scrolledtext.ScrolledText(client_frame, width=30, height=10, wrap='word')
        message_log.pack(padx=5, pady=10, side=RIGHT)


        # Creating a dedicated frame for security information.
        info_frame = ttk.LabelFrame(client_frame, text='Security Metadata', padding=10)
        info_frame.pack(fill='x', side=BOTTOM, pady=10)
        
        # This label will show the key currently being used
        self.key_display = ttk.Label(info_frame, text='Key: (Awaiting Connection...)',
                                     font=('Courier', 10), wraplength=400)
        self.key_display.pack()


        # Here we will add the button that will send data from the client to the server.
        # And the threading logic that will handle the listening loop.
        ttk.Button(client_frame, text='Send', command=handle_send).pack()
        threading.Thread(target=start_client_node, daemon=True).start()


    def open_server(self):
        """ This window will create a server node that will select between asymmetric and symmetric encyption methods
            It will establish a connection with the client. There will be a text entry to send messages to the client
            and there will be a scrolling text box to view messages in the message log. """
        
        # Instantiating a network object.
        self.server_network = SecureMessage()
        self.server_network.address = ('localhost', 6790)

        # Note that these are nested functions. start_server_node initializes the server and calls the listen_loop().
        # Note: SecureMessage.init_server() uses socket.accept() which is another listening loop, which waits for
        #       incomming connection. One thread then can handle both occurrences of the server listening loops.
        def start_server_node():
            self.server_network.init_server()
            self.root.after(0,update_key_label)
            listen_loop()


        def listen_loop():
            while True:
                msg = self.server_network.receive_data()
                if msg:
                    self.root.after(0, lambda m=msg: message_log.insert(END, f'Client: {m}\n'))


        def handle_send():
            msg = server_message.get('1.0', END).strip()
            if msg:
                self.server_network.send_data(msg)
                message_log.insert(END, f'You: {msg}\n')
                message_log.see(END)
                server_message.delete('1.0', END)

        
        def update_key_label():
            """ Helps to refresh the UI with an active key string using the SecureMessage.get_keys_info() method."""
            try:
                key_info = self.server_network.get_keys_info()
                server_info_label.config(text=key_info)
                print(f'DEBUG: Key Info is: {key_info[:20]}...')
            except Exception as e:
                print(f'DEBUG: Error updating label: {e}')

        server_window = Toplevel(self.root)
        server_window.title('Server Connection')

        server_frame = ttk.Frame(server_window, padding=20)
        server_frame.pack(expand=True, fill='both')                         
                                 
        ttk.Label(server_frame, text='Message Control', foreground='blue', font=('Roboto', 30)).pack(pady=10)
        ttk.Label(server_frame, text='Compose', foreground='blue', font=('Roboto', 20)).pack(pady=5, side=LEFT)
        ttk.Label(server_frame, text='Message Log', foreground='blue', font=('Roboto', 20)).pack(pady=5, side=RIGHT)
        server_message = Text(server_frame, width=30, height=10, wrap='word')
        server_message.pack(padx=5, pady=10, side=LEFT)
        message_log = scrolledtext.ScrolledText(server_frame, width=30, height=10, wrap='word')
        message_log.pack(padx=5, pady=10, side=RIGHT)

        # Creating a dedicated frame for security information.
        info_frame = ttk.LabelFrame(server_frame, text='Security Metadata', padding=10)
        info_frame.pack(fill='x', side=BOTTOM, pady=10)
        
        # This label will show the key currently being used
        server_info_label = ttk.Label(info_frame, text='Key: (Awaiting Connection...)',
                                     font=('Courier', 10), wraplength=400)
        server_info_label.pack()

        # Again we will add the 'Send' button which runs handle_send() to check for msg by getting server_message.
        ttk.Button(server_frame, text='Send', command=handle_send).pack()
        # We will create a similar threading object but this time we have placed the listen_loop() method inside 
        # of a start_server_node() method because the server requires an additional continuous loop living inside 
        # the init_server() method that can break the tkinter mainloop().
        threading.Thread(target=start_server_node, daemon=True).start()

class SecureMessage:
    """ This class is designed to handle establishing the network protocol and listening procedures. Threading will be
        utilized to provide concurrency between to continuosly looping processes."""
    
    # Creating the class attribute key outside of __init__ method allows me to share the symmetric keys without sending them unsecurely over the connection.
    master_sym_key = Fernet.generate_key()


    def __init__(self):
        self.address = ('localhost', 6789)
        self.max_size = 4096
        self.conn = None  # This will be used to store the active connection
        self.mode = 'asymmetric'     # Default encryption mode

        # Symmetric Setup
        self.sym_key = SecureMessage.master_sym_key
        self.cipher_suite = Fernet(self.sym_key)

        # Asymmetric Setup
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    
    def get_keys_info(self):
        """ Returns a str() repr of keys for the purposes of the assignment"""
        if self.mode == 'symmetric':
            return f'Symmetric Key: {self.sym_key.decode()}'
        else:
            pub_swap = self.public_key_swap.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
            return f'Asymmetric Public Key:\n{pub_swap[:100]}...'
        
    def encrypt(self, message):
        """ Encrypts based on the selected mode."""
        data = message.encode('utf-8')
        if self.mode == 'symmetric':
            return self.cipher_suite.encrypt(data)
        else:
            return self.public_key_swap.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        

    def decrypt(self, ciphertext):
        """ Decrypts based on the selected mode."""
        if self.mode == 'symmetric':
            return self.cipher_suite.decrypt(ciphertext).decode('utf-8')
        else:
            return self.private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode('utf-8')

    # Initialize client connection.
    def init_client(self):
        """ Establish the socket connection using tcp."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address)
        self.conn = self.client

        # Public key swap. Receive the server's public key first.
        server_pub_bytes = self.client.recv(self.max_size)
        self.public_key_swap = serialization.load_pem_public_key(server_pub_bytes)

        # Public key swap. Send client public key to the server.
        my_pub_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.client.send(my_pub_bytes)

        return 'Connected to Server'


    # Initialize the server connection.
    def init_server(self):
        """ Establish the socket connection usig tcp. """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.server.listen(1)
        # The accept() method blocks the mainloop(). To handle this, the init_server method
        # will be called via start_server_node() method inside of a thread.
        self.conn, addr = self.server.accept()

        # Public key swap. Sending server public key to the client.
        my_pub_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.conn.send(my_pub_bytes)

        # Public Key Swap. Receive the client's public key.
        client_pub_bytes = self.conn.recv(self.max_size)
        self.public_key_swap = serialization.load_pem_public_key(client_pub_bytes)

        return 'Connected to Client'


    # Handles the logic to send a message.
    def send_data(self, message):
        """ Sending encrypted text over the established connection"""
        if self.conn:
            encrypted = self.encrypt(message)       # Encrypts the message using the encrypt() method defined above.
            self.conn.send(encrypted)       # Encrypted message is passed via LoginApp.handle_send()

    # Handles the logic to receive an encrypted message and returns the decrypted message in 'utf-8' (handled in the decrypt() method above).
    def receive_data(self):
        """ Recieves a maximum of 4096 bits from connection and assigns to data object.
            Then calls the decrypt() method on the data object to return the utf-8 encoded string.
            Note that because this will be used to listen continously, this will block the mainloop()
            if threading is not utilized."""
        try:
            data = self.conn.recv(self.max_size)
            return self.decrypt(data) if data else None
        except Exception as e:
            print(f'Decryption error: {e}')
            return None



if __name__ == '__main__':
    root = Tk()
    app = LoginApp(root)
    root.mainloop()