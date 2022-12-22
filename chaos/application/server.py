"""API definition for churn detection."""
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from chaos.domain.customer import Customer
import pandas as pd
from typing import Optional, Literal
from datetime import datetime


class CustomerInput(BaseModel):
    """Churn detection parameters.

    Parameters
    ----------
    BALANCE : float
        customer bank account balance
    NB_PRODUITS : int
        how many products the customer owns
    CARTE_CREDIT : bool
        true if the customer has a credit card
    SALAIRE : float
        customer's salary
    SCORE_CREDIT : float
        customer score for credit allocation
    DATE_ENTREE : datetime
        optional (fot futur use), date of the customer subscription
        date in format "YYYY-MM-DD HH:MM"
    PAYS : str
        country of the customer
    SEXE : str
        customer's gender, 'H' (Male) of 'F' (Female)
    AGE : int
        customer's age
    MEMBRE_ACTIF:
        true if the customer is active on his bank account
    """

    BALANCE: float = None
    NB_PRODUITS: int = None
    CARTE_CREDIT: bool = None
    SALAIRE: float = None
    SCORE_CREDIT: float = None
    DATE_ENTREE: Optional[datetime] = None
    PAYS: str = None
    SEXE: Literal["H", "F"] = None
    AGE: int = None
    MEMBRE_ACTIF: bool = None


app = FastAPI(
    title="Churn detection",
    openapi_tags=[{
        "name": "detect",
        "description": ("Give a probability of churn "
                        "given customer's characteristics")
    }]
)


class Answer(BaseModel):
    """Churn detection response."""

    answer: float


@app.post("/detect/", tags=["detect"])
def detect(q: CustomerInput):
    """Call Customer model churn detection.

    Parameters
    ----------
    q : Question(BaseModel)
        Customer marketing characterics
    """
    customer = Customer(pd.DataFrame([q.dict()]))
    answer = customer.predict_subscription()

    return Answer(answer=answer)
