import typing
import strawberry
from sqlalchemy.orm import Session

import models
import database

@strawberry.type
class StudentType:
    id: int
    name: str
    email: str

@strawberry.type
class TopicType:
    id: int
    title: str
    category: str
    total_votes: int
    rounds: typing.List['RoundType']

@strawberry.type
class VoteType:
    id: int
    student_id: int
    topic_id: int

@strawberry.type
class ResultType:
    id: int
    topic_id: int
    total_votes: int

@strawberry.type
class RoundType:
    id: int
    topic_id: int
    round_number: int

@strawberry.input
class CastVoteInput:
    student_id: int
    topic_id: int

@strawberry.type
class CastVotePayload:
    id: typing.Optional[int]
    vote: typing.Optional[VoteType]
    error: typing.Optional[str]

@strawberry.type
class VoteWithTopicType:
    id: int
    student_id: int
    topic_id: int
    topic_title: str
    topic_category: str

@strawberry.type
class Query:
    @strawberry.field
    def topics(self, info: strawberry.Info, category: typing.Optional[str] = None) -> typing.List[TopicType]:
        db: Session = info.context["db"]
        query = db.query(models.Topic)
        if category:
            query = query.filter(models.Topic.category == category)
        
        topics = query.outerjoin(models.Result, models.Topic.id == models.Result.topic_id).order_by(models.Result.total_votes.desc().nulls_last()).all()
        
        return [
            TopicType(
                id=t.id, 
                title=t.title, 
                category=t.category,
                total_votes=t.result.total_votes if t.result else 0,
                rounds=[RoundType(id=r.id, topic_id=r.topic_id, round_number=r.round_number) for r in t.rounds]
            )
            for t in topics
        ]

    @strawberry.field
    def results(self, info: strawberry.Info, topic_id: int) -> typing.Optional[ResultType]:
        db: Session = info.context["db"]
        res = db.query(models.Result).filter(models.Result.topic_id == topic_id).first()
        if res:
            return ResultType(id=res.id, topic_id=res.topic_id, total_votes=res.total_votes)
        return None

    @strawberry.field
    def students(self, info: strawberry.Info, name: typing.Optional[str] = None) -> typing.List[StudentType]:
        """Fetch all students. Optionally filter by name (case-insensitive partial match)."""
        db: Session = info.context["db"]
        query = db.query(models.Student)
        if name:
            query = query.filter(models.Student.name.ilike(f"%{name}%"))
        return [
            StudentType(id=s.id, name=s.name, email=s.email)
            for s in query.all()
        ]

    @strawberry.field
    def student(self, info: strawberry.Info, id: int) -> typing.Optional[StudentType]:
        """Fetch a single student by their ID."""
        db: Session = info.context["db"]
        s = db.query(models.Student).filter(models.Student.id == id).first()
        if s:
            return StudentType(id=s.id, name=s.name, email=s.email)
        return None

    @strawberry.field
    def student_votes(self, info: strawberry.Info, student_id: int) -> typing.List[VoteWithTopicType]:
        """Fetch all votes cast by a specific student, including the topic details."""
        db: Session = info.context["db"]
        votes = db.query(models.Vote).filter(models.Vote.student_id == student_id).all()
        return [
            VoteWithTopicType(
                id=v.id,
                student_id=v.student_id,
                topic_id=v.topic_id,
                topic_title=v.topic.title,
                topic_category=v.topic.category
            )
            for v in votes
        ]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def cast_topic_vote(self, info: strawberry.Info, input: CastVoteInput) -> CastVotePayload:
        db: Session = info.context["db"]
        
        # Duplicate vote prevention
        existing_vote = db.query(models.Vote).filter(
            models.Vote.student_id == input.student_id,
        ).first()
        
        if existing_vote:
            return CastVotePayload(id=None, vote=None, error="Student has already voted.")
            
        topic = db.query(models.Topic).filter(models.Topic.id == input.topic_id).first()
        if not topic:
            return CastVotePayload(id=None, vote=None, error="Topic not found.")
            
        student = db.query(models.Student).filter(models.Student.id == input.student_id).first()
        if not student:
            return CastVotePayload(id=None, vote=None, error="Student not found.")
            
        new_vote = models.Vote(student_id=input.student_id, topic_id=input.topic_id)
        db.add(new_vote)
        
        # Update results
        result = db.query(models.Result).filter(models.Result.topic_id == input.topic_id).first()
        if not result:
            result = models.Result(topic_id=input.topic_id, total_votes=1)
            db.add(result)
        else:
            result.total_votes += 1
            
        db.commit()
        db.refresh(new_vote)
        
        return CastVotePayload(
            id=new_vote.id,
            vote=VoteType(id=new_vote.id, student_id=new_vote.student_id, topic_id=new_vote.topic_id),
            error=None
        )

schema = strawberry.Schema(query=Query, mutation=Mutation)
