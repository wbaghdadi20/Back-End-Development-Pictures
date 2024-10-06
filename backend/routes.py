from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item.get("id") == id), None)

    if picture is None:
        abort(404, description="Picture not found")

    return jsonify(picture), 200

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    
    picture_id = request.json["id"]
    picture = next((item for item in data if item["id"] == picture_id), None)
    
    if picture:
        return make_response(jsonify({"Message": f"picture with id {picture_id} already present"}), 302)

    new_picture = {
        "id": picture_id,
        "pic_url": request.json["pic_url"],
        "event_country": request.json["event_country"], 
        "event_state": request.json["event_state"], 
        "event_city": request.json["event_city"], 
        "event_date": request.json["event_date"] 
    }

    data.append(new_picture)
    return make_response(jsonify(new_picture), 201)

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture is None:
        return make_response(jsonify({"message": "picture not found"}), 404)

    picture["pic_url"] = request.json.get("pic_url", picture.get("pic_url"))
    picture["event_country"] = request.json.get("event_country", picture.get("event_country"))
    picture["event_state"] = request.json.get("event_state", picture.get("event_state"))
    picture["event_city"] = request.json.get("event_city", picture.get("event_city"))
    picture["event_date"] = request.json.get("event_date", picture.get("event_date"))

    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture is None:
        return make_response(jsonify({"message": "picture not found"}), 404)

    data.remove(picture)
    return "", 204