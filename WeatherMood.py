import requests
import sqlite3
import googlemaps

#Establishing Connection to Database
con = sqlite3.connect("C:\\Users\patri\\Desktop\\WeatherMood\\WeatherMood\\user.db")
cur = con.cursor()

#Updates location of user to current location
def UpdateLoc(user, city):
    cur.execute("UPDATE user SET location = REPLACE(location, '%s','%s') WHERE id=%s" % (user.loc, city, user.id))
    con.commit()
    user.loc = city
    return print(user.name + "'s location has been changed to '" + user.loc + "'")

def UpdateWeather(user):

    weatherData = requests.get("http://api.weatherapi.com/v1/current.json?key=ce694d555ff84cbbb3e122529220509&q=" + user.loc)
    weatherDict = weatherData.json()
    newWeather = weatherDict['current']['condition']['text']
    newTemp = weatherDict['current']['temp_f']
    print(newWeather)
    cur.execute("UPDATE user SET weather = REPLACE(weather, '%s','%s') WHERE id=%s" % (user.weather, newWeather, user.id))
    con.commit()
    cur.execute("UPDATE user SET temp = REPLACE(temp, '%s','%s') WHERE id=%s" % (user.temp, newTemp, user.id))
    con.commit()
    
    user.weather = newWeather
    user.temp = newTemp

    return print(user.name + "'s weather and temmperature has been changed to '" + user.weather + "'")

#Get users current location
def GetCurrentLoc():
    
    gmaps = googlemaps.Client(key='AIzaSyBF-KtkTNuBPSPLKRaar5Y_Wg55UO8tUG0')
    latLng = gmaps.geolocate()
    coord = latLng["location"]
    lat = coord["lat"]
    lng = coord["lng"]

    googleResponse = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=%s, %s&key=AIzaSyBF-KtkTNuBPSPLKRaar5Y_Wg55UO8tUG0" % (lat, lng))
    #print(googleResponse.status_code) #Check if api responds
    googleDict = googleResponse.json()
    #Gets users city
    currentCity = googleDict['results'][0]['address_components'][2]["long_name"] 
    return currentCity

#Delete user from database
def DeleteUser(user):
    delete = "DELETE FROM user WHERE id=?"
    cur.execute(delete, (user.id,))
    con.commit()
    return print("User '" + user.name + "' has been deleted")

#Adds User to Database
def AddUser(user):
    cur.execute("SELECT 1 FROM user WHERE id=%s" % user.id) #Open transaction
    if cur.fetchone():
        print("*** User already exists ***")
    else:
        cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)", (user.name, user.loc, user.weather, user.temp, user.id))
        con.commit() #Close transaction
        print("New User '" + user.name + "' has been added")

#Prints Database
def PrintDB(database):
    result = cur.execute("SELECT * FROM " + database)
    return print(result.fetchall())

#Defining User Class
class User:
    def __init__(self, name, loc, id, weather = "None", temp = 70):
        self.name = name
        self.loc = loc
        self.id = id
        self.weather = weather
        self.temp = temp

def main():
    ### Creating Table ###
    try:
        cur.execute("CREATE TABLE user(name, location, weather, temp, id)")
        print("Table created")
    except:
        print("Existing table used")

    Pat = User("Pat", "Bergen", 0)
    Austin = User("Austin", "Rochester", 1)
    Katrina = User("Katrina", "Medellin", 2)
    Ben = User("Ben", "Medellin", 3)

    AddUser(Katrina)
    AddUser(Ben)
    AddUser(Austin)
    AddUser(Pat)

    UpdateLoc(Ben, 'Bangkok')
    UpdateLoc(Pat, GetCurrentLoc())
    UpdateWeather(Pat)

    #DeleteUser(Ben)
    PrintDB("user")

if __name__ == "__main__":
    main()
