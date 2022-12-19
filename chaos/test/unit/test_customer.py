from chaos.domain.customer import Customer
from interpret.glassbox.ebm.ebm import ExplainableBoostingClassifier
import pandas as pd 
from chaos.domain.customer import Customer 


#TODO : Mockup of Socio-eco 
#TODO : pydantic on data input and output format 
#TODO : monkeypatch on connect, setattr init. 
#TODO : Factoriser le load du modèle, et faire changer la variable marketing qu'on lui donne.

def test_model_loading(mocker): 
    """ Here we check if the Customer will load the ChurnModel, and if it's pipeline contain the ExplainableBoostingClassifier"""
    customer = Customer(marketing={"A":1})
    assert isinstance (customer.model.pipe.get_params()['classifier'],ExplainableBoostingClassifier)
    


def test_model_prediction():
    marketing_dataframe =pd.read_json("chaos/test/data/random_marketing_input.json")
    customer = Customer(marketing=marketing_dataframe)
    predict_proba_serie = customer.predict_subscription()
    assert predict_proba_serie.values[0] == True