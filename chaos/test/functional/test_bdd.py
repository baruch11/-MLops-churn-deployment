from sqlalchemy.engine.base import Engine
from chaos.infrastructure.connexion import Connexion
import pandas as pd
import datetime

expected_data = {"id_client": [15688172],
                 "date_entree": [datetime.date(2015, 6, 1)],
                 "nom": ["Tai"],
                 "pays": ["Espagne"],
                 "sexe": ["H"],
                 "age": [40],
                 "membre_actif": ["No"],
                 "balance": [0.0],
                 "nb_produits": [2],
                 "carte_credit": ["Yes"],
                 "salaire": [88947.56],
                 "score_credit": [677.0],
                 "churn": ["No"]
                 }


class TestDatabase:
    def test_to_connect(self):
        connexion = Connexion().connect(sqlalchemy_engine=True)
        assert isinstance(
            connexion,
            Engine
        )

    def test_select_customer(self):
        query = "SELECT COUNT (*) FROM customer"
        connexion = Connexion().connect(sqlalchemy_engine=True)
        data = pd.read_sql(query, connexion)
        assert data.values[0][0] == 9950

    def test_select_indicators(self):
        query = "SELECT COUNT (*) FROM indicators"
        connexion = Connexion().connect(sqlalchemy_engine=True)
        data = pd.read_sql(query, connexion)
        assert data.values[0][0] == 9950

    def test_select_join(self):

        query = "SELECT customer.ID_CLIENT, DATE_ENTREE, NOM, PAYS, SEXE, AGE,\
             MEMBRE_ACTIF, BALANCE, NB_PRODUITS, CARTE_CREDIT, \
                SALAIRE, SCORE_CREDIT, CHURN\
                FROM customer\
                INNER JOIN indicators ON \
                    customer.ID_CLIENT=indicators.ID_CLIENT;"
        connexion = Connexion().connect(sqlalchemy_engine=True)
        data = pd.read_sql(query, connexion)
        line_15688172 = data.loc[data["id_client"] == 15688172]
        expected_df = pd.DataFrame(data=expected_data)
        assert expected_df.equals(line_15688172)
