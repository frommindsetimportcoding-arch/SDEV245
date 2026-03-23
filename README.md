M01 Assignment - RBAC and Authenitication Mini App
  This application provides confidentiality because it searches through the users currently on file and only allows access into the admin endpoint or the user endpoint if the password credentials entered match the case. It also assesses what role has
  been given to each specific user and this determines which endpoint to connect to. The way that the code is set up, you should not be able to gain access to the admin panel or user panel if you first don't match the credentials on file. Then you you with
  be subject to authorization which in turn opens the correct endpoint for you. If you are not in the system, a generic error message is politely prompted. 
  
  In a sense there is integrity because the app doesn't allow for any input of data on the separate endpoints, haha. Integrity is the trustworthiness of the information. The goal is to prevent a bad actor from having the ability to manipulate your data or to 
  delete it altogether. 
  
  Availability ensures that the information is safe from threats like DDOS which overloads a service until it crashes. 
  
  The objective is to remember these three concepts when securing an application and to concern oneself with them at every step of the process. I believe that the more often you consider these conditions, you not only lessen the likelihood of leaving a hack
  to be discovered, but you may also discover a more secure method for the future. 
