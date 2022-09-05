import requests
import sqlite3

response = requests.get("http://api.weatherapi.com/v1/current.json?key=ce694d555ff84cbbb3e122529220509&q=Rochester")
#print(response.status_code)

#print(response.json())


#Database
con = sqlite3.connect("user.db")
cursor = con.cursor()

try:
    cursor.execute("CREATE TABLE user(name, location, id)")
    print("Table created")
except:
    print("Existing table used")



#Open transaction
cursor.execute("SELECT EXISTS(SELECT 1 FROM user WHERE id=1)")
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

result = cursor.execute("SELECT * FROM user")

print(result.fetchall())



dict = response.json()
loc = dict["location"]
name = loc["name"]

def UpdateLoc(user, name):
    user.loc = name
    return print(user.loc)


class User:
    def __init__(self, name, loc, id):
        self.name = name
        self.loc = loc
        self.id = id

Pat = User("Pat", "Mahopac", 0)
Austin = User("Austin", "Rochester", 1)
Katrina = User("Katrina", "Medellin", 2)


#UpdateLoc(Pat, name)