"""API definition for churn detection."""
import logging
import os
import tempfile
from fastapi import FastAPI
from pydantic import BaseModel
from chaos.domain.customer import Customer
from typing import Optional, Literal
from datetime import datetime
from google.cloud import storage
import pickle
from chaos.infrastructure.config.config import config


def load_churn_model():
    """Load churn model from GCS.

    Returns
    -------
        ChurnModelFinal
    """
    bucket_name = config["gcs"]["bucket"]
    source_blob_name = config["gcs"]["blob"]

    logging.info("Loading model %s from GCS",
                 bucket_name+"/"+source_blob_name)

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    model = None
    with tempfile.TemporaryDirectory() as tmpdirname:
        destination_file_name = os.path.join(
            tmpdirname, "ChurnModelFinal.pkl")
        blob.download_to_filename(destination_file_name)
        with open(destination_file_name, "rb") as model_pkl:
            model = pickle.load(model_pkl)

    return model


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
    customer = Customer(customer_input.dict(), get_global_churn_model())
    answer = customer.predict_subscription()

    return Answer(answer=answer)
