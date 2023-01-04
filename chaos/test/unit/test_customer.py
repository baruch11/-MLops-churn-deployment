import pytest
from chaos.domain.customer import Customer
from interpret.glassbox.ebm.ebm import ExplainableBoostingClassifier
from unittest import TestCase
from chaos.infrastructure.socio_eco import SocioEco
from churn.domain.churn_model import ChurnModelFinal

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
        customer = Customer(marketing={"A": 1},
                            model=ChurnModelFinal.load())
        assert isinstance(
            customer.model.pipe.get_params()['classifier'],
            ExplainableBoostingClassifier)

    @pytest.mark.parametrize(
        "marketing, expected",
        [({"BALANCE": 93259.57, "NB_PRODUITS": 3, "CARTE_CREDIT": "Yes",
           "SALAIRE": 141035.65, "SCORE_CREDIT": 581.0,
           "DATE_ENTREE": "2015-01-01 00:00:00", "NOM": "Mazzi",
           "PAYS": "Allemagne", "SEXE": "F", "AGE": 43,
           "MEMBRE_ACTIF": "No"}, True)])
    def test_model_prediction(self, marketing, expected):
        """ Here we provide an object corresponding to a customer, and we
                verify that the prediction worked, and that the output is True.
        """

        customer = Customer(marketing, ChurnModelFinal.load())
        predict_proba_serie = customer.predict_subscription()
        TestCase().assertTrue((predict_proba_serie.values[0] > 0.5) == expected)


class TestSocioEco:
    def test_instantiate_socio_eco(self, mock_socio_eco):
        """ We can init a SocioEco instance who need a connection, but we have
        # mocked it thanks to the function mock_socio_eco """
        socio_eco = SocioEco()
        assert isinstance(socio_eco, SocioEco)