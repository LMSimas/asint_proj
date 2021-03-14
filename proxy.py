from flask import Flask, abort
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify, url_for
from flask import session

from datetime import datetime

import requests


#necessary so that our server does not need https
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "supersekrit"  # Replace this with your own secret!
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
fenix_blueprint = OAuth2ConsumerBlueprint(
    "fenix-example", __name__,
    # this value should be retrived from the FENIX OAuth page
    client_id="1132965128044781",
    # this value should be retrived from the FENIX OAuth page
    client_secret="6B0xfGStwNk5MpPPYJsu3DoeaLptLDWgCoV5apJKRHM8JLNJ/Y/Buvpww/iotMLgqq3oDQqmVfhS1WMRtsyzOw==",
    # do not change next lines
    base_url="https://fenix.tecnico.ulisboa.pt/",
    token_url="https://fenix.tecnico.ulisboa.pt/oauth/access_token",
    authorization_url="https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
)
app.register_blueprint(fenix_blueprint)


administrators = ["ist187124", "ist187058"]
#professor inserts here the ist number
####WEB PAGES###

@app.route('/')
def home_page():
    try:
        if fenix_blueprint.session.authorized == True: #if user is logged in
            try: 
                #get user information
                user = getUser() 
                #register user
                try:
                    #user_added = requests.post(url="http://127.0.0.1:8005/API/users/", json=user)
                    user_added = requests.post(url="http://127.0.0.1:8002/API/users/", json=user)
                except:
                    user_added = requests.post(url="http://127.0.0.1:8005/API/users/", json=user)
                if user_added.text == "User Created":
                    #Register a creation of a user in log events
                    now = datetime.now()
                    timestamp = now.strftime('%Y-%b-%d %H:%M:%S')
                    message = {"data_type": "User", "content": str(user), "timestamp": timestamp, "user_id": user["user_id"]}
                    requests.post(url="http://127.0.0.1:8004/API/logs/events/", json=message)
                    sendMtoLogs(user_added)
                return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized, administrators = administrators, username=user['user_id'], user_info = user_added.text)
            except:
                token = fenix_blueprint.token['access_token']
                expire = fenix_blueprint.token['expires_at']
                #fenix_blueprint.session.access_token = str(fenix_blueprint.token['refresh_token'])

                #Probably the token as expired, need to logout and login again
                return redirect(url_for("logout"))
        else:
            return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized)
    except:
        abort(400)

@app.route('/video_list')
def video_list():
    try:
        return render_template("video_list.html", loggedIn = fenix_blueprint.session.authorized)
    except:
        abort(400)

@app.route('/logs')
def logs_page():
    try:
        return render_template("logs_Page.html")
    except:
        abort(400)

@app.route('/users_Page')
def users_page():
    try:
        return render_template("users_page.html")
    except:
        abort(400)

@app.route('/logout')   
def logout():
    try:
        # this clears all server information about the access token of this connection
        res = str(session.items())
        session.clear()
        res = str(session.items())
        # when the browser is redirected to home page it is not logged in anymore
        return redirect(url_for("home_page"))
    except:
        abort(400)

####API Videos###
@app.route('/API/videos/',methods=['GET','POST'])
def get_videos():
    try:
        user = {}
        if request.method == 'GET':
            #getting the list of videos
            response = requests.get(url="http://127.0.0.1:8001/API/videos/")
            sendMtoLogs(response)
        elif request.method == 'POST':
            user = getUser()
            video = request.get_json()
            video["user_id"]= user["user_id"]

            #adding a new video for a user
            try:            
                response = requests.post(url="http://127.0.0.1:8002/API/users/newMusic/", json = video)
                #response1 = requests.post(url="http://127.0.0.1:8005/API/users/newMusic/", json = video)
            except:
                response = requests.post(url="http://127.0.0.1:8005/API/users/newMusic/", json = video)
            sendMtoLogs(response)

            #adding a video in the database
            response = requests.post(url="http://127.0.0.1:8001/API/videos/", json=video)
            sendMtoLogs(response)

        return response.text
    except:
        abort(400)

@app.route("/API/videos/<int:id>/" , methods=['GET', 'POST'])
def single_video(id):
    try:
        if request.method == 'POST': 
            #Delete a video
            response = requests.post(url="http://127.0.0.1:8001/API/videos/"+str(id)+"/")
            result = response.json()
            sendMtoLogs(response)
            return result
        elif request.method == 'GET':
            user = getUser()
            global first_displayID
            first_displayID = id
            #new view for that video
            response = requests.post(url="http://127.0.0.1:8001/API/videos/"+str(id)+"/addNewView/")
            sendMtoLogs(response)
            #new view for that user
            try:
                response = requests.post(url="http://127.0.0.1:8002/API/users/newView/", json =  user)
                #response1 = requests.post(url="http://127.0.0.1:8005/API/users/newView/", json = user)
            except:
                response = requests.post(url="http://127.0.0.1:8005/API/users/newView/", json = user)
            sendMtoLogs(response)

            #request to get the url and user id of the video
            response = requests.get(url="http://127.0.0.1:8001/API/videos/"+str(id)+"/")
            result = response.json()
            sendMtoLogs(response)

            return render_template("video_page.html", video_id = id, url = result["url"], user = result["user_id"]) 
        return ''
    except:
        abort(400)

####API Users###
@app.route('/API/users/')
def user_stat():
    try:
        #getting the list of users
        try:
            
            response = requests.get(url="http://127.0.0.1:8002/API/users/")
            #response1 = requests.get(url="http://127.0.0.1:8005/API/users/")
        except:
            response = requests.get(url="http://127.0.0.1:8005/API/users/")
        sendMtoLogs(response)
        return response.text
    except:
        abort(400)

@app.route('/API/users/login')
def user_login():
    try:
        try :
            
            response = requests.get(url = "http://127.0.0.1:8002/API/users/login" )
            #response1 = requests.get(url="http://127.0.0.1:8005/API/users/login")
        except:
            response = requests.get(url="http://127.0.0.1:8005/API/users/login")
        return redirect(url_for(response.text))
    except:
        abort(400)
    
####API QA###
@app.route('/API/QA/<int:video_id>/questions/', methods=['GET', 'POST'])
def get_Questions(video_id):
    try:
        myobj = {'video_id': video_id}
        user = {}
        if request.method == 'GET':
            #get the questions for a video
            response = requests.get(url="http://127.0.0.1:8003/API/questions/"+str(video_id)+"/")
            result = response.json()
            sendMtoLogs(response)
            return result
        elif request.method == 'POST':
            #ask a question for a video
            user = getUser()
            question = request.get_json()
            question["user_id"] = user["user_id"]
            response = requests.post(url="http://127.0.0.1:8003/API/questions/"+str(video_id)+"/", json = question)
            result = response.json()
            sendMtoLogs(response)
            response = requests.post(url="http://127.0.0.1:8001/API/videos/"+str(video_id)+"/""addNewQuestion/")
            sendMtoLogs(response)
            try:
                
                response = requests.post(url="http://127.0.0.1:8002/API/users/newQuestion/", json = user)
                #response1 = requests.post(url="http://127.0.0.1:8005/API/users/newQuestion/", json = user)
            except:
                response = requests.post(url="http://127.0.0.1:8005/API/users/newQuestion/", json = user)
            sendMtoLogs(response)
            return result
        return ''
    except:
        abort(400)

@app.route('/API/QA/questions/<int:id>/', methods=['GET', 'POST'])
def answers(id):
    try:
        if request.method == 'GET':
            response = requests.get(url="http://127.0.0.1:8003/API/answers/"+str(id)+"/")
            result = response.json()
            sendMtoLogs(response)
            return result
        elif request.method == 'POST':
            user = getUser()
            answer = request.get_json()
            answer["user_id"] = user["user_id"]
            answer["user_name"] = user["name"]
            response = requests.post(url="http://127.0.0.1:8003/API/answers/"+str(id)+"/", json = answer)
            result = response.json()
            sendMtoLogs(response)
            try:
                
                response = requests.post(url="http://127.0.0.1:8002/API/users/newAnswer/", json = user)
                #response1 = requests.post(url="http://127.0.0.1:8005/API/users/newAnswer/", json = user)
            except:
                response = requests.post(url="http://127.0.0.1:8005/API/users/newAnswer/", json = user)
            sendMtoLogs(response)
            
            return result
        return ''
    except:
        abort(400)

@app.route('/API/QA/questions/getUser/', methods=['GET', 'POST'])
def getUserFromQuestion():
    try:
        question = request.get_json()
        response = requests.get(url="http://127.0.0.1:8003/API/QA/getUser/", json = question)
        sendMtoLogs(response)
        return response.text
    except:
        abort(400)

####API Logs###
@app.route('/API/logs/')
def logs():
    try:
        ret = requests.get(url="http://127.0.0.1:8004/API/logs/")
        return ret.text
    except:
        abort(400)

@app.before_request
def before_request_func():
    count = 0
    now = datetime.now()
    timestamp = now.strftime('%Y-%b-%d %H:%M:%S')
    if "favicon" not in request.path:
        message = {"ip": request.host, "endpoint": request.path, "timestamp": timestamp}
        requests.post(url="http://127.0.0.1:8004/API/logs/messages/", json=message)
    
@app.after_request
def after_request_func(response):
    try:
        count = 0
        now = datetime.now()
        timestamp = now.strftime('%Y-%b-%d %H:%M:%S')
        if '/API/videos/' in request.url:
            for char in request.url:
                if char == '/':
                    count +=1
            if count == 5:
                if request.method == 'POST':
                    print('create a video')
                    user = getUser()
                    message = {"data_type": "Video", "content": str(request.json), "timestamp": timestamp, "user_id": user["user_id"]}
                    requests.post(url="http://127.0.0.1:8004/API/logs/events/", json=message)
            elif count == 6:
                if request.method == 'POST':
                    print('delete video')
                    user = getUser()
                    message = {"data_type": "Video", "content": str(request.json), "timestamp": timestamp, "user_id": user["user_id"]}
                    requests.post(url="http://127.0.0.1:8004/API/logs/events/", json=message)
        elif '/API/QA/' in request.url:
            if '/API/QA/questions/getUser/' in request.url:
                pass
            elif '/API/QA/questions/' in request.url:
                if request.method == 'POST':
                    print('new answer for question')
                    user = getUser()
                    message = {"data_type": "Answer", "content": str(request.json), "timestamp": timestamp, "user_id": user["user_id"]}
                    requests.post(url="http://127.0.0.1:8004/API/logs/events/", json=message)
            else:
                if request.method == 'POST':
                    print('new question for video')
                    user = getUser()
                    message = {"data_type": "Question", "content": str(request.json), "timestamp": timestamp, "user_id": user["user_id"]}
                    requests.post(url="http://127.0.0.1:8004/API/logs/events/", json=message)
        return response
    except:
        abort(400)

#Function to get user details provided by fenix
def getUser():
    try:
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        data = resp.json()
        user = {'user_id': data['username'], 'name': data['name']}
        return user
    except:
        abort(400)
#Function to send the logs messages to db
def sendMtoLogs(response):
    try:
        x = response.url.split("/",3)
        now = datetime.now()
        timestamp = now.strftime('%Y-%b-%d %H:%M:%S')
        message = {"ip": x[2], "endpoint": "/" + x[3], "timestamp": timestamp}
        requests.post(url="http://127.0.0.1:8004/API/logs/messages/", json=message)
    except:
        abort(400)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
