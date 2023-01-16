from sqlalchemy.engine.base import Engine
from chaos.infrastructure.customer_loader import CustomerLoader
from chaos.application.server import app
from fastapi.testclient import TestClient
import pandas as pd
import numpy as np

expected_data = {"ID_CLIENT": [15688172],
                 "DATE_ENTREE": [np.datetime64("2015-06-01")],
                 "NOM": ["Tai"],
                 "PAYS": ["Espagne"],
                 "SEXE": ["H"],
                 "AGE": [40],
                 "MEMBRE_ACTIF": ["No"],
                 "BALANCE": [0.0],
                 "NB_PRODUITS": [2],
                 "CARTE_CREDIT": ["Yes"],
                 "SALAIRE": [88947.56],
                 "SCORE_CREDIT": [677.0],
                 "CHURN": ["No"]
                 }


class TestCustomerLoader:

    def test_instantiate_customer_loader(self):
        customer_loader = CustomerLoader()
        assert isinstance(
            customer_loader.engine,
            Engine
        )

    def test_load_all_customer_data(self):
        customer_loader = CustomerLoader()
        all_raw_data = customer_loader.load_all_customer_raw()
        assert all_raw_data.shape == (199, 13)

    def test_find_a_specific_customer(self):
        customer_loader = CustomerLoader()
        line_15688172 = customer_loader.find_a_customer(15688172)
        expected_df = pd.DataFrame(data=expected_data)
        assert expected_df.equals(line_15688172)
    
    def test_predict_from_id(self):
        with TestClient(app) as client: 
            response = client.get("/customer_detect/15791700")
            assert response.status_code == 200 
            assert response.json()["answer"] == 0.9769012533043302

        
