from flask import Flask, abort, request,  redirect, url_for
from Video_DB import *

app = Flask(__name__)


@app.route("/API/videos/", methods = ['GET', 'POST'])
def returnsVideosJSON(): 
    if request.method == 'GET':
        return {"videos": listVideosDICT()}
    elif request.method == 'POST':
        video = request.get_json()
        ret = False
        try:
            #print(video["description"])
            ret = newVideo(video["description"], video['url'], video['user_id'])
        except:
            abort(400)
            #the arguments were incorrect
        if ret:
            return {"id": ret}
        else:
            abort(409)

@app.route("/API/videos/<int:id>/" , methods=['GET','POST'])
def SingleVideoJSON(id):
    if request.method == 'GET':
        try:
            v = getVideoDICT(id)
            return v
        except:
            abort(404)
    elif request.method == 'POST':
        try:
            #print(video["videoID"])
            ret = deleteVideo(id)
        except:
            abort(400)
            #the arguments were incorrect
        if ret:
            return {"result": ret}
        else:
            abort(409)

@app.route("/API/videos/<int:id>/addNewQuestion/", methods=['POST'])
def NewQuestionToVideo(id):
    try:
        newVideoQuestion(id)
        return ''
    except:
        abort(404)


@app.route("/API/videos/<int:id>/addNewView/", methods=['POST'])
def NewViewToVideo(id):
    try:
        newVideoView(id)
        return ''
    except:
        abort(404)
    

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8001, debug=True)
