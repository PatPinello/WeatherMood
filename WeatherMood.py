import requests
import sqlite3

response = requests.get("http://api.weatherapi.com/v1/current.json?key=ce694d555ff84cbbb3e122529220509&q=Rochester")
#print(response.status_code) #Check response
con = sqlite3.connect("user.db")
cursor = con.cursor()

def UpdateLoc(user, name):
    user.loc = name
    return print(user.loc)

def InsertDB(user):
    cursor.execute("INSERT INTO user VALUES (?, ?, ?)", (user.name, user.loc, user.id))
    return print("User inserted")

def PrintDB(database):
    result = cursor.execute("SELECT * FROM " + database)
    return print(result.fetchall())

class User:
    def __init__(self, name, loc, id):
        self.name = name
        self.loc = loc
        self.id = id

try:
    cursor.execute("CREATE TABLE user(name, location, id)")
    print("Table created")
except:
    print("Existing table used")

#Open transaction
cursor.execute("SELECT 1 FROM user WHERE id=0")
if cursor.fetchone():
    print("User already exists")
else:

    cursor.execute("""
        INSERT INTO user VALUES
            ("Pat", "Mahopac", 0),
            ("Austin", "Rochester", 1)
                """)
    #Close transaction
    con.commit()

dict = response.json()
loc = dict["location"]
name = loc["name"]

Pat = User("Pat", "Mahopac", 0)
Austin = User("Austin", "Rochester", 1)
Katrina = User("Katrina", "Medellin", 2)

InsertDB(Katrina)
PrintDB("user")

#UpdateLoc(Pat, name)