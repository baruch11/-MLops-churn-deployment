"""API definition for churn detection."""
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from chaos.domain.customer import Customer
from chaos.infrastructure.customer_loader import CustomerLoader
import pandas as pd
from typing import Optional, Literal
from datetime import datetime, date


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


class BddCustomerOutput(BaseModel):
    id_client: int
    date_entree: date
    nom: str
    pays: str
    sexe: str
    age: int
    membre_actif: str
    balance: float
    nb_produits: int
    carte_credit: str
    salaire: float
    score_credit: float
    churn: str


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
def detect(customer_input: CustomerInput):
    """Call Customer model churn detection.

    Parameters
    ----------
    customer_input : CustomerInput(BaseModel)
        Customer marketing characterics
    """

    customer = Customer(customer_input.dict())
    answer = customer.predict_subscription()

    return Answer(answer=answer)


@app.get("/customer/{customer_id}")
def read_item(customer_id):
    customer_loader = CustomerLoader()
    df_prospect = customer_loader.find_a_customer(customer_id)
    dict_prospect = df_prospect.to_dict(orient="records")[0]
    bdd_customer_output = BddCustomerOutput(**dict_prospect)
    return bdd_customer_output
