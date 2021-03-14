from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path

from sqlalchemy.sql.sqltypes import Float


#SLQ access layer initialization
DATABASE_FILE = "qa.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False, connect_args={'check_same_thread': False}) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Question(Base):
    __tablename__ = 'Question'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer)
    time = Column(Float)
    user_id = Column(String)
    text = Column(String)
    def __repr__(self):
        return "<Question (Video_id=%d Time=%f, User_id=%s, Text=%s>" % (
                                self.video_id, self.time, self.user_id, self.text)
    def to_dictionary(self):
        return {"question_id": self.id,"video_id": self.video_id, "time": self.time, "user_id": self.user_id, "text": self.text}

class Answer(Base):
    __tablename__ = 'Answer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    user_id = Column(String)
    user_name = Column(String)
    text = Column(String)
    def __repr__(self):
        return "<Answer (User_id=%s, User_name=%s, Text=%s, QuestionID=%d>" % (
                                self.user_id, self.user_name, self.text, self.question_id)
    def to_dictionary(self):
        return {"user_id": self.user_id, "user_name": self.user_name, "text": self.text, "question_id": self.question_id}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()

# QUESTIONS FUNCTIONS---------------------------------------------------------------
def listQuestions():
    try:
        return session.query(Question).all()
        session.close()
    except:
        abort(409)

def listQuestionsDICT():
    try:
        ret_list = []
        lv = listQuestions()
        for v in lv:
            vd = v.to_dictionary()
            ret_list.append(vd)
        return ret_list
    except:
        abort(409)

def getQuestions(id):
    try:
        ret_list = []
        #order = session.query(Question).order_by(Question.time).all()
        lv =  session.query(Question).filter(Question.video_id==id).order_by(Question.time).all()
        for v in lv:
            question = v.to_dictionary()
            ret_list.append(question)
        session.close()
        return ret_list
    except:
        abort(409)

def getQuestionDICT(id):
    try:
        return getQuestions(id).to_dictionary()
    except:
        abort(409)


def newQuestion(video_id , time, user_id, text):
    
    quest = Question(video_id = video_id, time = time, user_id = user_id, text = text)
    try:
        session.add(quest)
        session.commit()
        # print(quest.id)
        session.close()
        return "New Question added!"
    except:
        print("error adding the question")
        return None
        
def getUser(video_id_query, time_query, text_query):
    info ={}
    a = session.query(Question).filter(Question.video_id==int(video_id_query)).filter(Question.time == time_query).filter(Question.text==text_query).first()
    question = a.to_dictionary()
    try:
        info['user_id'] = question['user_id']
        info['question_id'] = question['question_id']
        return info
    except:
        return "No question"



# ANSWERS FUNCTIONS---------------------------------------------------------------
def newAnswer(text, user_id, user_name, question_id):
    answer = Answer(text = text, user_id = user_id, user_name = user_name, question_id = question_id)
    try:
        session.add(answer)
        session.commit()
        session.close()
        return "\nNew Answer added!\n"
    except:
        print("\n\nError\n\n")
        return None

def getAnswers(questionID): #ver qual o melhor input pra filtrar a answers
    try:
        ret_list = []
        lv =  session.query(Answer).filter(Answer.question_id==questionID).all()
        for v in lv:
            answer = v.to_dictionary()
            ret_list.append(answer)
        session.close()
        return ret_list
    except:
        abort(409)

if __name__ == "__main__":
    pass