"""API definition for churn detection."""
from fastapi import FastAPI
from pydantic import BaseModel
from chaos.domain.customer import (Customer, load_churn_model,
                                   ModelNotFoundException)
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
    CARTE_CREDIT : str ("Yes" or "No")
        'Yes' if the customer has a credit card
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
    MEMBRE_ACTIF: str ('Yes' or 'No')
        'Yes' if the customer is active on his bank account
    """

    BALANCE: float = None
    NB_PRODUITS: int = None
    CARTE_CREDIT: Literal["Yes", "No"] = None
    SALAIRE: float = None
    SCORE_CREDIT: float = None
    DATE_ENTREE: Optional[datetime] = None
    PAYS: str = None
    SEXE: Literal["H", "F"] = None
    AGE: int = None
    MEMBRE_ACTIF: Literal["Yes", "No"] = None


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


CHURN_MODEL_NOT_FOUND = -1
CHURN_MODEL_IS_LOADED = False
CHURN_MODEL = None


def get_global_churn_model():
    """Return global variable churn model and load it if not loaded."""
    if not CHURN_MODEL_IS_LOADED:
        CHURN_MODEL = load_churn_model()
    return CHURN_MODEL


@app.post("/detect/", tags=["detect"])
def detect(customer_input: CustomerInput):
    """Call Customer model churn detection.

    Parameters
    ----------
    customer_input : CustomerInput(BaseModel)
        Customer marketing characterics
    """
    try:
        model = get_global_churn_model()
    except ModelNotFoundException:
        return Answer(answer=CHURN_MODEL_NOT_FOUND)
    customer = Customer(customer_input.dict(), model)
    answer = customer.predict_subscription()

    return Answer(answer=answer)
