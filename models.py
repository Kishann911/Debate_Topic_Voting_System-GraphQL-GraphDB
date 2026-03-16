from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String, index=True)  # social, political

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"))

    student = relationship("Student")
    topic = relationship("Topic")

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"))
    total_votes = Column(Integer, default=0)

    topic = relationship("Topic")

class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"))
    round_number = Column(Integer)

    topic = relationship("Topic")
