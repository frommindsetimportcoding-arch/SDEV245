"""
Creating a basic app that demonstrates the core ideas of authentication, roles and access control.

I think I am going to try to do this using tkinter. I am using tkinter v 8.6.15
"""
import tkinter as tk
from tkinter import *
from tkinter import ttk


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

# Start the program



user_roles = {'admin': ['lovelace', 'knuth'],
              'user': ['bob', 'jerry']}
credentials = {'lovelace': 'ada', 'knuth': 'donald', 'bob':'bob', 'jerry':'jerry'}          # I used dictionaries to contain my authentication and authorization information. 
# error_label = None    This is a work in progress. 

def authenticate(user, password):
    """ This function aims to receive the username and password entry and compare it to the credentials dictionary. 
        If the username is in the dictionary, it will move forward to the next if statement. It then compares the password entered
        with the password on file. If all is well, then we begin the authorization by calling the authorize() function. 
        If either instance fails, a generic error message is displayed. Unfortunately the error message is displayed once it compares to 'lovelace'
        and fails the check in the iteration.
        
        I can workaround this by hiding the login window and deleting the label in the background. And deiconifying it when I close out of one of the Toplevel() windows.
        I want to figure out how to add it to the command as a second function for the button. 
        I was running out of time to pretty it up and wanted to make sure that I submitted an application that met the requirements of the assignment."""
    
    for entry in credentials:
        if user == entry:
            pw = credentials[entry]
            if password == pw:
                authorize(user)
                break
            else:
                ttk.Label(mainframe, text='Invalid Username and Password', foreground='red').grid(column=3, row=1, sticky=E)
        else:
            ttk.Label(mainframe, text='Invalid Username and Password', foreground='red').grid(column=3, row=1, sticky=E)
    
def authorize(user):
    if user in user_roles['admin']:
        open_admin()
    elif user in user_roles['user']:
        open_user()

def open_admin():
    """ This creates a toplevel window that opens the administrative panel with 'top secret stuff'. I created this by referencing the documents and tutorials referenced in the documents.
        I will need to add more child widgets and play with the padding to really have a good idea of how the padding effects the GUI, so that I can better document my work. """

    # root.withdraw()
    admin_window = Toplevel(root)
    admin_window.title('Administrative Panel')
    # admin_window.geometry('300x100') I will need to learn how to center my grid, if possible. 
    
    admin_frame = ttk.Frame(admin_window, padding=(3, 3, 12, 12))
    admin_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    
    ttk.Label(admin_frame, text='This is top-secret stuff here!', foreground='purple', font='Roboto').grid(column=1, row=1, sticky=(W, E))
    ttk.Button(admin_frame, text='Close', command=admin_window.destroy).grid(column=1, row=2, sticky=(W, E))   # I want to add my deiconify logic here. 
    
    admin_window.columnconfigure(0, weight=1)
    admin_window.rowconfigure(0, weight=1)
    
    admin_frame.columnconfigure(2, weight=1)
    for child in admin_frame.winfo_children:
        child.grid_configure(padx=5, pady=15)


def open_user():
    """ This creates a toplevel window that opens the user panel with 'Jerry and Bob stuff'. I created this by referencing the documents and tutorials referenced in the documents.
        I will need to add more child widgets and play with the padding to really have a good idea of how the padding effects the GUI, so that I can better document my work. """

    # root.withdraw()  Can't use this yet. Not without deiconify

    user_window = Toplevel(root)
    user_window.title('User Panel')
    
    user_frame = ttk.Frame(user_window, padding=(3, 3, 12, 12))
    user_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    
    ttk.Label(user_frame, text='This is for Jerry and Bob.', foreground='green', font='Roboto').grid(column=1, row=1, sticky=(W, E))
    ttk.Button(user_frame, text='Close', command=user_window.destroy).grid(column=1, row=2, sticky=(W, E))      # I want to add my deiconify logic here.
    
    user_window.columnconfigure(0, weight=1)
    user_window.rowconfigure(0, weight=1)
    
    user_frame.columnconfigure(2, weight=1)
    for child in user_frame.winfo_children:
        child.grid_configure(padx=5, pady=15)


root = Tk()
# if error_label is not None:
#     error_label.destroy()
#     error_label = None

root.title('User Login')   # Sets the title of the window


mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))     # Child element of the root. Frame widget with padding.
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))    

user = StringVar()      # Allows for variable input as string
user_entry = ttk.Entry(mainframe, width=10, textvariable=user)  # Child of mainframe. Variable name assigned as user.
user_entry.grid(column=2, row=1, sticky=(W, E))

password = StringVar()
password_entry = ttk.Entry(mainframe, width=10, textvariable=password)  # Child of mainframe. Variable name assigned as password. 
password_entry.grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text='Log In', command=lambda: authenticate(user.get(), password.get())).grid(column=3, row=3, sticky=W)   # Button initiates event that calls authenticate() with user, password parameters

ttk.Label(mainframe, text='Username: ').grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text='Password: ').grid(column=1, row=2, sticky=E)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

user_entry.focus()
root.bind('<Return>', lambda event: authenticate(user.get(), password.get()))  # Binds the return key to the same event as the button click. 




#
# I want to refactor this logic into a single class, but I didn't have enough time to figure it out before the assignment was due.
#
# class App:
#     def __init__(self, root):
#         self.root = root
#         self.login()
#         self.error_label = None

#     def login(self):
#         if self.error_label is not None:
#             self.error_label.destroy()
#             self.error_label = None

#         self.root.title('User Login')


#         self.mainframe = ttk.Frame(self.root, padding=(3, 3, 12, 12))
#         self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

#         self.user = StringVar()
#         self.user_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.user)
#         self.user_entry.grid(column=2, row=1, sticky=(W, E))

#         self.password = StringVar()
#         self.password_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.password)
#         self.password_entry.grid(column=2, row=2, sticky=(W, E))

#         ttk.Button(self.mainframe, text='Log In', command=lambda: authenticate(self.user.get(), self.password.get())).grid(column=3, row=3, sticky=W)

#         ttk.Label(self.mainframe, text='Username: ').grid(column=1, row=1, sticky=E)
#         ttk.Label(self.mainframe, text='Password: ').grid(column=1, row=2, sticky=E)

#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         self.mainframe.columnconfigure(2, weight=1)
#         for child in self.mainframe.winfo_children():
#             child.grid_configure(padx=5, pady=5)

#         self.user_entry.focus()
#         self.root.bind('<Return>', lambda event: authenticate(self.user.get(), self.password.get()))


#     def authenticate(self, user, password):
#         for entry in credentials:
#             if self.user == entry:
#                 print('she is in here')
#                 pw = credentials[entry]
#                 if password == pw:
#                     print('password is good')
#                     self.authorize(user)
#                     break
#                 else:
#                     print('password not good')
#                     ttk.Label(self.mainframe, text='Invalid Username and Password', foreground='red').grid(column=3, row=1, sticky=E)
#             else:
#                 print('not here')
#                 ttk.Label(self.mainframe, text='Invalid Username and Password', foreground='red').grid(column=3, row=1, sticky=E)
root.mainloop()