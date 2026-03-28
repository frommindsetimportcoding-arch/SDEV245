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
from tkinter import ttk


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


    def close_panel(self, window):
        """ Destroys the top window and unhides the login screen."""
        window.destroy()
        self.username_var.set('')   # Clears the fields before bringing the login window back.
        self.password_var.set('')
        self.root.deiconify()       # Brings the login screen back.

    
    def open_login(self):
        """ Allows for opening the login window without destroying the current window.
            This is necessary so that I can use the separate windows as a client and 
            server for encrypted messaging."""
        self.username_var.set('')
        self.password_var.set('')
        self.root.deiconify()


if __name__ == '__main__':
    root = Tk()
    app = LoginApp(root)
    root.mainloop()