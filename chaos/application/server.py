from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

DEFAULT_RESPONSE = 0


class Question(BaseModel):
    question: float = 0


class Answer(BaseModel):
    answer: float


@app.post("/example/")
def example(q: Question):
    try:
        answer = q.question * 2
    except (ValueError, TypeError, KeyError):
        answer = DEFAULT_RESPONSE
    return Answer(answer=answer)
