from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "ytVideos.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False, connect_args={'check_same_thread': False}) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class YTVideo(Base):
    __tablename__ = 'YTVideo'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    user_id = Column(String)
    url = Column(String)
    questions = Column(Integer, default = 0)
    views = Column(Integer, default = 0)
    def __repr__(self):
        return "<YouTubeVideo (id=%d Description=%s, URL=%s, User=%s, Questions=%s Views=%s>" % (
                                self.id, self.description, self.url, self.user_id,  self.questions, self.views)
    def to_dictionary(self):
        return {"video_id": self.id, "description": self.description, "url": self.url, "user_id": self.user_id, "questions": self.questions, "views": self.views}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listVideos():
    return session.query(YTVideo).all()
    session.close()

def listVideosDICT():
    try:
        ret_list = []
        lv = listVideos()
        for v in lv:
            vd = v.to_dictionary()
            del(vd["url"])
        #del(vd["questions"])
            ret_list.append(vd)
        return ret_list
    except:
        return None

def getVideo(id):
    try:
        v =  session.query(YTVideo).filter(YTVideo.id==id).first()
        session.close()
        return v
    except:
        return None

def deleteVideo(id):
     a =session.query(YTVideo).filter(YTVideo.id==id).delete()
     session.commit()
     session.close()
     if a == 0:
         return "Could not Delete the requested video!"
     else:
        return "The video was deleted!"

def getVideoDICT(id):
    try:
        return getVideo(id).to_dictionary()
    except:
        return None

def newVideoQuestion(id):
    b = session.query(YTVideo).filter(YTVideo.id==id).first()
    b.questions+=1
    try:
        session.commit()
        session.close()
        return "question increment sucess!"
    except:
        return None

def newVideoView(id):
    b = session.query(YTVideo).filter(YTVideo.id==id).first()
    b.views+=1
    try:
        session.commit()
        session.close()
        return "views increment sucess!"
    except:
        return None

def newVideo(description , url, user_id):
    vid = YTVideo(description = description, user_id = user_id, url = url)
    try:
        session.add(vid)
        session.commit()
        print(vid.id)
        session.close()
        return vid.id
    except:
        return None


if __name__ == "__main__":
    pass