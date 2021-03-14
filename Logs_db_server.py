from flask import Flask, abort, request,  redirect, url_for
from Logs_DB import *

app = Flask(__name__)


@app.route("/API/logs/", methods = ['GET', 'POST'])
def returnsLogsJSON():
    try: 
        if request.method == 'GET':
            return {"events": listEventsDICT(), "messages": listMessagesDICT()}
    except:
        abort(409)


@app.route("/API/logs/messages/" , methods=['POST'])
def createMessage():
    message = request.get_json()
    ret = False
    try:
        ret = newMessage(message["ip"], message['endpoint'], message['timestamp'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"result": ret}
    else:
        abort(409)

@app.route("/API/logs/events/" , methods=['POST'])
def createEvent():
    event = request.get_json()
    ret = False
    try:
        ret = newEvent(event["data_type"], event['content'], event['timestamp'], event['user_id'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        print("\n I WILL ADDD\n")
        return {"result": ret}
    else:
        print("\n ERROOOOss\n")
        abort(409)


if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8004, debug=True)
