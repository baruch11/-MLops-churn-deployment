"""Customer model."""
import os
from churn.domain.churn_model import ChurnModelFinal
import pandas as pd

this_dir = os.path.dirname(os.path.realpath(__file__))


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
            self.model = ChurnModelFinal().load()

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
