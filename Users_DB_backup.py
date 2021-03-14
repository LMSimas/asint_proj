from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "users_backup.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False,connect_args={'check_same_thread': False}) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class AppUser(Base):
    __tablename__ = 'AppUser'
    ist_id = Column(String, primary_key=True)
    name = Column(String)
    n_vid = Column(Integer, default = 0)
    n_que = Column(Integer, default = 0)
    n_ans = Column(Integer, default = 0)
    n_views = Column(Integer, default = 0)
    def __repr__(self):
        return "<User (IST_id=%s Name=%s Videos Registered=%d Number of Questions=%d Number of Answers =%d Number of views =%d" % (
                                self.ist_id, self.name, self.n_vid, self.n_que, self.n_ans, self.n_views)
    def to_dictionary(self):
        return {"IST_id": self.ist_id, "Name": self.name, "N_videos": self.n_vid, "N_questions": self.n_que, "N_answers": self.n_ans, "N_views": self.n_views}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)

def listUsers():
    try:
        return session.query(AppUser).all()
        session.close()
    except:
        abort(409)

def listUsersDICT():
    try:
        ret_list = []
        lv = listUsers()
        for u in lv:
            vd = u.to_dictionary()
            ret_list.append(vd)
        return ret_list
    except:
        abort(409)

def getUser(ist_id):
    try:
        u =  session.query(AppUser).filter(AppUser.ist_id==ist_id).first()
        session.close()
        return u
    except:
        abort(409)

def getUserDICT(ist_id):
    try:
        return getUser(ist_id).to_dictionary()
    except:
        abort(409)

def newVideoAdd(ist_id):
    b = session.query(AppUser).filter(AppUser.ist_id==ist_id).first()
    b.n_vid+=1
    try:
        session.commit()
        session.close()
        return "Music Added"
    except:
        abort(409)

def newQuestionAdd(ist_id):
    b = session.query(AppUser).filter(AppUser.ist_id==ist_id).first()
    b.n_que+=1
    try:
        session.commit()
        session.close()
        return "Question Added"
    except:
        abort(409)

def newAnswerAdd(ist_id):
    b = session.query(AppUser).filter(AppUser.ist_id==ist_id).first()
    b.n_ans+=1
    try:
        session.commit()
        session.close()
        return "Answer Added"
    except:
        abort(409)

def newViewAdd(ist_id):
    b = session.query(AppUser).filter(AppUser.ist_id==ist_id).first()
    b.n_views+=1
    try:
        session.commit()
        session.close()
        return "View Added"
    except:
        abort(409)


def newUser(ist_id, name):
    add_user = 0
    us = AppUser(ist_id = ist_id, name = name)
    try:
        exists = session.query(AppUser).filter(AppUser.ist_id==ist_id).first()
        exists.ist_id
    except:
        add_user = 1
    
    if add_user == 1:
        try:
            session.add(us)
            session.commit()
            session.close()
            return "User Created"
        except:
            return "Error when creating User"
    else:
        return "User already exists"

if __name__ == "__main__":
    pass