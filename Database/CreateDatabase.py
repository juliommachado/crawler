from Connection import Connection

''' This should be created using something more powerful for a crawler, like mongodb.
    But for now I'm doing everything with my sparetime in a place with a lot of restrictions,
    so sqlite will be usefull for a while. '''

#Just Creating the file    
file = open('database.db', 'w+')
file.close()

  
connection = Connection('database.db')
connection.execute('CREATE TABLE Url (id INTEGER PRIMARY KEY, url TEXT)')
connection.execute('CREATE TABLE Page (id INTEGER PRIMARY KEY, url_id INTEGER, html TEXT, is_parsed BOOLEAN, FOREIGN KEY(url_id) REFERENCES Url(id))')