from fastapi import FastAPI
from pydantic import BaseModel
from chaos.domain.customer import Customer
import pandas as pd

app = FastAPI()

DEFAULT_RESPONSE = -1


class Question(BaseModel):
    BALANCE: float = 0.0
    NB_PRODUITS: int = 0
    CARTE_CREDIT: bool = True
    SALAIRE: float = 0.0
    SCORE_CREDIT: float = 0.0
    DATE_ENTREE: str = "2010"
    NOM: str = ""
    PAYS: str = 'France'
    SEXE: bool = False
    AGE: int = 40
    MEMBRE_ACTIF: bool = False


class Answer(BaseModel):
    answer: float


@app.post("/example/")
def example(q: Question):
    try:
        customer = Customer(pd.DataFrame([q.dict()]))
        answer = customer.predict_subscription()
    except (ValueError, TypeError, KeyError):
        answer = DEFAULT_RESPONSE
    return Answer(answer=answer)
