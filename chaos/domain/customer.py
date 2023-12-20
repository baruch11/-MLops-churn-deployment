"""Customer model."""
import logging
import os
import tempfile
import pickle
import pandas as pd
from google.cloud import storage
import google.cloud.exceptions as ggexp
from chaos.infrastructure.config.config import config

this_dir = os.path.dirname(os.path.realpath(__file__))


class ModelNotLoaded(Exception):
    """Model not found."""


class Customer:
    """Class representing a bank customer."""

    def __init__(self, marketing: dict, model=None):
        """Class representing a bank customer.

        Parameters
        ----------
        marketing: dict
            marketing data, used as features for prediction.
        model: ChurnModelFinal
            optional model
        """
        self.marketing = marketing
        self.model = model
        if self.model is None:
            raise ModelNotLoaded

    def predict_subscription(self) -> float:
        """Return appetence score [0,1] of the customer predicted by the model.

        Returns
        -------
        appetence: float
            appetence of the customer to the bank loan (0: not appetent, 1:
                very appetent)

        Explanation
        -----------
        We construct the features from the caracteristics and the socio
        economic data. At the moment, we use arbitrary features.
        This should be changed.
        """
        predict_proba = self.model.predict_proba(pd.DataFrame([self.marketing]))
        return predict_proba


def load_churn_model():
    """Load churn model from GCS.

    Returns
    -------
        ChurnModelFinal
    """
    bucket_name = config["gcs"]["bucket"]
    source_blob_name = config["gcs"]["blob"]
    gcp_project = config["gcs"]["project"]

    logging.info("Loading model %s from GCS",
                 bucket_name+"/"+source_blob_name)

    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    model = None
    with tempfile.TemporaryDirectory() as tmpdirname:
        destination_file_name = os.path.join(
            tmpdirname, "ChurnModelFinal.pkl")
        try:
            blob.download_to_filename(destination_file_name)
            with open(destination_file_name, "rb") as model_pkl:
                model = pickle.load(model_pkl)
        except ggexp.NotFound:
            logging.error("%s not found in %s", source_blob_name, bucket_name)
            raise ModelNotLoaded

    return model
