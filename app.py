import json
import uuid

from flask import Flask
from flask import request, render_template, jsonify

from anime import Anime
from character import Character
from VA import VA
from errors import register_error_handlers


app = Flask(__name__)
register_error_handlers(app)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/anime", methods = ["POST"])
def add_anime():
    anime_data = request.get_json(force=True, silent=True)
    if anime_data == None:
        return "Bad request", 400
    anime = Anime(anime_data["title"], anime_data["image"], anime_data["studio"], anime_data["episodes"], anime_data["seasons"], None)
    anime.save()
    return json.dumps(anime.to_dict()), 201
    
@app.route("/character", methods = ["POST"])
def add_character():
    char_data = request.get_json(force=True, silent=True)
    if char_data == None:
        return "Bad request", 400
    character = Character(char_data["name"], char_data["image"], char_data["anime"], char_data["VA"], None)
    character.save()
    return json.dumps(character.to_dict()), 201

@app.route("/VA", methods = ["POST"])
def add_VA():
    va_data = request.get_json(force=True, silent=True)
    if va_data == None:
        return "Bad request", 400
    va = VA(va_data["name"], va_data["image"], None)
    va.save()
    return json.dumps(va.to_dict()), 201

@app.route("/anime", methods = ["GET"])
def list_anime():
    result = {"result": []}
    for anime in Anime.all():
        result["result"].append(anime.to_dict())
    return json.dumps(result)

@app.route("/VA", methods = ["GET"])
def list_VAs():
    result = {"result": []}
    for va in VA.all():
        result["result"].append(va.to_dict())
    return json.dumps(result)

#@app.route("/ads/<ad_id>", methods = ["GET"])
#def get_ad(ad_id):
#    return json.dumps(Ad.find_by_id(ad_id).to_dict())


@app.route("/anime/<title>", methods = ["GET"])
def view_anime(title):
    return render_template("anime.html", anime=Anime.find_by_title([title]))

@app.route("/character/<name>", methods = ["GET"])
def view_character(name):
    return render_template("character.html", character=Character.find_by_name([name]))

@app.route("/VA/<name>", methods = ["GET"])
def view_VA(name):
    return render_template("VA.html", va=VA.find_by_name([name]))

@app.route("/anime/<title>", methods = ["DELETE"])
def remove_anime(title):
    anime_data = request.get_json(force=True, silent=True)
    if anime_data == None:
        return "Bad request", 400

    anime = Anime.find_by_title([title])
    
    Anime.delete([title])
    return ""

@app.route("/character/<name>", methods = ["DELETE"])
def remove_character(name):
    char_data = request.get_json(force=True, silent=True)
    if char_data == None:
        return "Bad request", 400

    character = Character.find_by_name([name])
    
    Character.delete([name])
    return ""

@app.route("/VA/<name>", methods = ["DELETE"])
def remove_VA(name):
    va_data = request.get_json(force=True, silent=True)
    if va_data == None:
        return "Bad request", 400

    va = VA.find_by_name([name])
    
    VA.delete([name])
    return ""

@app.route("/anime/<title>", methods = ["PATCH"])
def update_anime(title):
    anime_data = request.get_json(force=True, silent=True)
    if anime_data == None:
        return "Bad request", 400

    anime = Anime.find_by_title([title])
    
    if "title" in anime_data:
        anime.title = anime_data["title"]
    if "studio" in anime_data:
        anime.studio = anime_data["studio"]
    if "episodes" in anime_data:
        anime.episodes = anime_data["episodes"]
    if "seasons" in anime_data:
        anime.seasons = anime_data["seasons"]
    return json.dumps(anime.save().to_dict())

@app.route("/character/<name>", methods = ["PATCH"])
def update_character(name):
    char_data = request.get_json(force=True, silent=True)
    if char_data == None:
        return "Bad request", 400

    character = Character.find_by_name([name])
    
    if "name" in char_data:
        character.name = char_data["name"]
    if "anime" in char_data:
        character.anime = char_data["anime"]
    if "VA" in char_data:
        character.VA = char_data["VA"]
    return json.dumps(character.save().to_dict())

@app.route("/VA/<name>", methods = ["PATCH"])
def update_VA(name):
    va_data = request.get_json(force=True, silent=True)
    if va_data == None:
        return "Bad request", 400

    va = VA.find_by_name([name])
    
    if "name" in va_data:
        va.name = va_data["name"]
    return json.dumps(va.save().to_dict())

#@app.route("/users/<user_id>", methods = ["GET"])
#def get_user(user_id):
#    return json.dumps(User.find_by_id(user_id).to_dict())


#@app.route("/users", methods = ["GET"])
#def list_users():
#    result = {"result": []}
#    for user in User.all():
#        result["result"].append(user.to_dict())
#    return json.dumps(result)


#@app.route("/users/<user_id>", methods = ["PATCH"])
#def change_user_info(user_id):
#    user_data = request.get_json(force=True, silent=True)
#    if user_data == None:
#        return "Bad request", 400

#    user = User.find_by_id(user_id)
#    if "username" in user_data:
#        user.username = user_data["username"]
#    if "address" in user_data:
#        user.address = user_data["address"]
#    if "phone_number" in user_data:
#        user.phone_number = user_data["phone_number"]
#    return json.dumps(user.save().to_dict())


#@app.route("/users/<user_id>", methods = ["DELETE"])
#def delete_user(user_id):
#    User.delete(user_id)
#    return ""


#@app.route("/users/purchased", methods = ["GET"])
#@require_login
#def list_purchased(user_id):
#    return json.dumps(Ad.find_all_purchased(user_id))
    

if __name__ == '__main__':
    app.run()

