from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, date

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://marcwil:hOJu0fwOFSkD379q@cluster0.upfx3.mongodb.net/Tank_DB?retryWrites=true&w=majority"
mongo = PyMongo(app)

#Globals
global user_object
user_object = {

        "username" : "default",
        "favourite_colour" : "default",
        "role" : "default",
        "last_updated" : "default"
    }

TANK_DB = []    # Database for Tank Objects
Id = 0


# Homepage
@app.route("/home", methods =["GET"])
def home():
	return "Homepage"

# GET Profile 
@app.route("/profile", methods =["GET"])
def display_user():
	return  jsonify(user_object)

# POST Profile 
@app.route("/profile", methods = ["POST"])
def post():

    # Only allows one user profile to be posted
    if user_object["username"] != "default":
        return "A user profile has already been registered"

    u = request.json["username"]
    f = request.json["favourite_colour"]
    r = request.json["role"]

    #Get current time - Snippet from : https://www.programiz.com/python-programming/datetime/current-time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()

    #Updating the Global user_object
    row = {"username" : u}
    user_object.update(row)
    row = {"favourite_colour" : f}
    user_object.update(row)
    row = {"role" : r}
    user_object.update(row)
    row = {"last_updated" : f"{today}, {current_time}"}
    user_object.update(row)

    return jsonify(user_object)

# PATCH Profile 
@app.route("/profile", methods = ["PATCH"])
def patch_user():
    
    #Get current time - Snippet from : https://www.programiz.com/python-programming/datetime/current-time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()


    row = {"last_updated" : f"{today}, {current_time}"}
    user_object.update(row)


    request_data = request.get_json()
    if 'username' in request_data:
        user_object["username"] = request_data["username"]
    if 'favourite_colour' in request_data:
        user_object["favourite_colour"] = request_data["favourite_colour"]
    if 'role' in request_data:
        user_object["role"] = request_data["role"]

    return jsonify(user_object)

#------------------------ Tank Routes -----------------------

# GET Tanks 
@app.route("/data", methods =["GET"])
def display_tanks():
	return  jsonify(TANK_DB)

# POST Tanks
@app.route("/data", methods = ["POST"])
def post_tank():
    loc = request.json["location"]
    lat = request.json["latitude"]
    long = request.json["longitude"]
    p = request.json["percentage_full"]
   
    global Id
    Id+=1
    tank_object = {
        "id": Id,
        "location": loc,
        "latitude": lat,
        "longitude": long,
        "percentage_full": p
    }
    TANK_DB.append(tank_object)
    return jsonify(tank_object)

# PATCH Tank
@app.route("/data/<int:id>", methods = ["PATCH"])
def patch_tank(id):
    for u in TANK_DB:
        if u["id"] == id:
            request_data = request.get_json()
            if 'location' in request_data:
                u["location"] = request_data["location"]
            if 'latitude' in request_data:
                u["latitude"] = request_data["latitude"]
            if 'longitude' in request_data:
                u["longitude"] = request_data["longitude"]
            if 'percentage_full' in request_data:
                u["percentage_full"] = request_data["percentage_full"]
            return jsonify(u)
    
    return "Tank ID not found"

# DELETE Tank 
@app.route("/data/<int:id>", methods =["DELETE"])
def delete_tank(id):
    for u in TANK_DB:
        if u["id"] == id:
            TANK_DB.remove(u)
            return "Success"

    return "Tank ID not found"

# API running loop
if __name__ == '__main__':
	app.run(
		debug = True,
		port = 3000,
		host="0.0.0.0"
    )