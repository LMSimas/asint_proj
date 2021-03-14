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
DATABASE_FILE = "logs.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False, connect_args={'check_same_thread': False}) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Message_Exchanged(Base):
    __tablename__ = 'Message_Exchanged'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    endpoint = Column(String)
    timestamp = Column(String)
    def __repr__(self):
        return "<Question (Log_id=%d Ip=%s, Endpoint=%s, Time=%s>" % (
                                self.id, self.ip, self.endpoint, self.timestamp)
    def to_dictionary(self):
        return {"log_id": self.id,"ip": self.ip, "endpoint": self.endpoint, "timestamp": self.timestamp}

class Event_Created(Base):
    __tablename__ = 'Event_Created'
    id = Column(Integer, primary_key=True)
    data_type = Column(String)
    content = Column(String)
    timestamp = Column(String)
    user_id = Column(String)
    def __repr__(self):
        return "<Answer (Log_id=%d, data_type=%s, content=%s, timestamp=%s, user_id=%s>" % (
                                self.id, self.data_type, self.content, self.timestamp, self.user_id)
    def to_dictionary(self):
        return {"log_id": self.id, "user_id": self.user_id, "data_type": self.data_type, "content": self.content, "timestamp": self.timestamp}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()

# Event_Created FUNCTIONS---------------------------------------------------------------
def listEvents():
    try:
        return session.query(Event_Created).all()
        session.close()
    except:
        abort(409)

def listEventsDICT():
    try:
        ret_list = []
        #lv = listEvents()
        lv = session.query(Event_Created).order_by(Event_Created.id.desc()).all()
        i=0
        for v in lv:
            if i==20:
                break
            vd = v.to_dictionary()
            ret_list.append(vd)
            i+=1
        return ret_list
    except:
        abort(409)

def newEvent(data_type , content, timestamp, user_id): 
    event = Event_Created(data_type = data_type, content = content, timestamp = timestamp, user_id = user_id)
    try:
        session.add(event)
        session.commit()
        # print(quest.id)
        session.close()
        return "New Event added!"
    except:
        print("error adding the Event")
        return None


# MEssage FUNCTIONS---------------------------------------------------------------

def listMessages():
    try:
        return session.query(Message_Exchanged).all()
        session.close()
    except:
        abort(409)

def listMessagesDICT():
    try:
        ret_list = []
        #lv = listMessages()
        lv = session.query(Message_Exchanged).order_by(Message_Exchanged.id.desc()).all()
        i = 0
        for v in lv:
            if i==20:
                break
            vd = v.to_dictionary()
            ret_list.append(vd)
            i+=1
        return ret_list
    except:
        abort(409)

def newMessage(ip, endpoint, timestamp):
    message = Message_Exchanged(ip = ip, endpoint = endpoint, timestamp = timestamp)
    try:
        session.add(message)
        session.commit()
        session.close()
        return "\nNew Message added!\n"
    except:
        return None


if __name__ == "__main__":
    pass