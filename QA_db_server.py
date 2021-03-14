from flask import Flask, abort, request,  redirect, url_for
from QA_DB import *

app = Flask(__name__)


@app.route("/API/questions/<int:id>/", methods = ['GET', 'POST'])
def returnsVideosJSON(id):
    if request.method == 'GET':
        try:
            return {"questions":  getQuestions(id)}
        except:
            abort(409)
    elif request.method == 'POST':
        try: 
            question = request.get_json()
            #print(question)
            result = newQuestion( question['video_id'], question['time'], question['user_id'], question['text'])
            #print("Result = ", result)
            ret = {"result": result}
            return ret
        except:
            abort(400)
    return ''


@app.route('/API/QA/getUser/')
def getUserFromQuestion():
    try:
        question = request.get_json()
        result = getUser(question['video_id'], question['time'], question['text'])
        return result
    except:
        abort(402)

@app.route("/API/answers/<int:id>/", methods = ['GET', 'POST'])
def answersJSON(id):
    if request.method == 'GET':
        try:
            return {"answers": getAnswers(id)}
        except:
            abort(409)
    elif request.method == 'POST':
        try: 
            answer = request.get_json()
            result = newAnswer( answer['text'], answer['user_id'], answer['user_name'], answer['question_id'])
            ret = {"result": result}
            return ret
        except:
            abort(409)
    return ''


if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8003, debug=True)
