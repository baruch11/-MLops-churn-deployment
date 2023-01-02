"""Customer model."""
import os
from churn.domain.churn_model import ChurnModelFinal
import pandas as pd

this_dir = os.path.dirname(os.path.realpath(__file__))


class Customer:

    def __init__(self, marketing: dict):
        """
        Parameters
        ----------
        marketing: dict
            marketing data, used as features for prediction. At the moment,
            only the following keys are used: 'AGE', 'BALANCE'
        """
        self.marketing = marketing
        self.model = ChurnModelFinal().load()

    def predict_subscription(self) -> float:
        """Returns appetence score [0,1] of the customer predicted by the model

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
        # TODO : Create a predict proba method on churnfinalmodel
        # TODO : pydantic on the output of the model.  We want a value between
        #  0.0 and 1.0, not boolean.
        predict_proba = self.model.predict_proba(pd.DataFrame([self.marketing]))
        return predict_proba

