from chaos.domain.customer import Customer
from interpret.glassbox.ebm.ebm import ExplainableBoostingClassifier
from unittest import TestCase
import pandas as pd
import numpy as np
from chaos.infrastructure.socio_eco import SocioEco


# TODO : pydantic on data input and output format
# TODO : monkeypatch on connect, setattr init.
# TODO : Factoriser le load du modèle, et faire changer la variable marketing
#  qu'on lui donne.


def do_nothing(self):
    pass


class TestModel(object):

    def test_model_loading(self):
        """ Here we check if the Customer will load the ChurnModel, and if it's
        pipeline contain the ExplainableBoostingClassifier"""
        customer = Customer(marketing={"A": 1})
        assert isinstance(
            customer.model.pipe.get_params()['classifier'],
            ExplainableBoostingClassifier)

    def test_model_prediction(self):
        """ Here we provide an object corresponding to a customer, and we
                verify that the prediction worked, and that the output is True.
        """
        marketing_dataframe = pd.read_json(
            "chaos/test/data/random_marketing_input.json"
            )
        customer = Customer(marketing=marketing_dataframe)
        predict_proba_serie = customer.predict_subscription()
        assert predict_proba_serie.values[0] is np.True_


class TestSocioEco(object):

    def test_instantiate_socio_eco(mock_socio_eco):
        """ We can init a SocioEco instance who need a connection, but we have
        # mocked it thanks to the function mock_socio_eco """

        socio_eco = SocioEco()
        assert isinstance(socio_eco, SocioEco)
