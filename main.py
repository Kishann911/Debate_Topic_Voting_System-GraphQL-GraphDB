from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from schema import schema

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Debate Voting System")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_context(db: Session = Depends(get_db)):
    return {"db": db}

graphql_app = GraphQLRouter(
    schema,
    context_getter=custom_context
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "Welcome to Debate Voting System. Go to /graphql for the IDE."}
