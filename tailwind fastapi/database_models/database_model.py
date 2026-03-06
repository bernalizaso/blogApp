from sqlalchemy import Integer, String, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

entry_tag = Table(
    "entry_tag",
    Base.metadata,
    Column("entry_id", Integer, ForeignKey("Entry.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("Tag.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    entries = relationship("Entry", back_populates="author")

class Entry(Base):
    __tablename__ = "Entry"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    tittle = Column(String) 
    content = Column(String)
    user_id = Column(Integer, ForeignKey("User.id"))
    author = relationship("User", back_populates="entries")
    tags = relationship("Tag", secondary=entry_tag, back_populates="entries")

class Tag(Base):
    __tablename__ = "Tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    entries = relationship("Entry", secondary=entry_tag, back_populates="tags")