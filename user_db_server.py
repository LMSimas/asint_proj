from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify, url_for
from flask import session
import time
from Users_DB import *
import requests

app = Flask(__name__)

@app.route("/API/users/", methods = ['GET', 'POST'])
def returnsVideosJSON():
    if request.method == 'GET':
        return {"users":  listUsersDICT()}
    elif request.method == 'POST': 
        user = request.get_json()
        ret = False
        try:
            ret = newUser(user['user_id'], user['name'])
        except:
            abort(400)
            #the arguments were incorrect
        return ret


@app.route("/API/users/newMusic/", methods = ['POST'])
def newMusicAdded():
    user = request.get_json()
    ret = False
    try:
        ret = newVideoAdd(user['user_id'])
    except:
        abort(400)
    return ret

@app.route("/API/users/newQuestion/", methods = ['POST'])
def newQuestionAdded():
    user = request.get_json()
    ret = False
    try:
        ret = newQuestionAdd(user['user_id'])
    except:
        abort(400)
    return ret

@app.route("/API/users/newAnswer/", methods = ['POST'])
def newAnswerAdded():
    user = request.get_json()
    ret = False
    try:
        ret = newAnswerAdd(user['user_id'])
    except:
        abort(400)
    return ret

@app.route("/API/users/newView/", methods = ['POST'])
def newViewAdded():
    user = request.get_json()
    ret = False
    try:
        ret = newViewAdd(user['user_id'])
    except:
        abort(400)
    return ret

@app.route("/API/users/login")
def login_user():
    return "fenix-example.login"

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8002, debug=True)
