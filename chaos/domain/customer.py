import os
import pickle

import numpy as np

from chaos.infrastructure.socio_eco import SocioEco

this_dir = os.path.dirname(os.path.realpath(__file__))


class Customer:
    MODEL_PATH = os.path.join(this_dir, "model.pkl")

    def __init__(self, marketing: dict):
        """
        Parameters
        ----------
        marketing: dict
            marketing data, used as features for prediction. At the moment, only the following keys are used: 'AGE', 'BALANCE'
        """
        self.marketing = marketing

        with open(self.MODEL_PATH, "rb") as handle:
            self.model = pickle.load(handle)

    def predict_subscription(self) -> float:
        """Returns appetence score [0,1] of the customer predicted by the model
        
        Returns
        -------
        appetence: float
            appetence of the customer to the bank loan (0: not appetent, 1: very appetent)

        Explanation
        -----------
        We construct the features from the caracteristics and the socio economic data.
        At the moment, we use arbitrary features. This should be changed.
        """
        # TODO: all the code below should be changed.
        # It's only a skeleton to show how to mix marketing and socio eco data for prediction
        socio_eco = SocioEco().read().iloc[0]["EMPLOYMENT_VARIATION_RATE"]
        age = self.marketing["AGE"]
        balance = self.marketing["BALANCE"]
        features = np.array((age, balance, socio_eco))
        appetence = self.model.predict_proba(features.reshape(1, -1))
        return appetence[0][1]
