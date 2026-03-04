from sqlalchemy import Integer, String, Float, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Entry(Base):

    __tablename__ = "Entry"

    id= Column(Integer, index = True, primary_key=True)
    date = Column(String)
    tittle = Column(String)
    content = Column(String)


   