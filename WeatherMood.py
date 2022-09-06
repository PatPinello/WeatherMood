import requests
import sqlite3
import googlemaps


#Getting Users Location
gmaps = googlemaps.Client(key='AIzaSyBF-KtkTNuBPSPLKRaar5Y_Wg55UO8tUG0')
latLng = gmaps.geolocate()
coord = latLng["location"]
lat = coord["lat"]
lng = coord["lng"]

googleResponse = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=%s, %s&key=AIzaSyBF-KtkTNuBPSPLKRaar5Y_Wg55UO8tUG0" % (lat, lng))
#print(googleResponse.status_code) #Check if api responds
googleDict = googleResponse.json()

#Gets users city
city = googleDict['results'][0]['address_components'][2]["long_name"] 

weather = requests.get("http://api.weatherapi.com/v1/current.json?key=ce694d555ff84cbbb3e122529220509&q=" + city)

#Database
con = sqlite3.connect("user.db")
cur = con.cursor()

#Updates location of user
def UpdateLoc(user, currentCity):
    user.loc = currentCity
    cur.execute("Update user set location = location where id = %s" % user.id)
    con.commit()
    return print(user.loc)

#Adds User to Database
def AddUser(user):
    cur.execute("SELECT 1 FROM user WHERE id=%s" % user.id) #Open transaction
    if cur.fetchone():
        print("*** User already exists ***")
    else:
        cur.execute("INSERT INTO user VALUES (?, ?, ?)", (user.name, user.loc, user.id))
        con.commit() #Close transaction

#Prints Database
def PrintDB(database):
    result = cur.execute("SELECT * FROM " + database)
    return print(result.fetchall())

#Defining User Class
class User:
    def __init__(self, name, loc, id):
        self.name = name
        self.loc = loc
        self.id = id

### Creating Table ###
try:
    cur.execute("CREATE TABLE user(name, location, id)")
    print("Table created")
except:
    print("Existing table used")

dict = weather.json()

Pat = User("Pat", "Mahopac", 0)
Austin = User("Austin", "Rochester", 1)
Katrina = User("Katrina", "Medellin", 2)
Ben = User("Ben", "Medellin", 3)

AddUser(Katrina)
UpdateLoc(Ben, 'Rome')
PrintDB("user")
#print(Ben.loc)