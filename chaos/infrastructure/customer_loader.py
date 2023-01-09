import pandas as pd
import string
from datetime import datetime

from chaos.infrastructure.connexion import Connexion


class CustomerLoader:

    def __init__(self):
        self.engine = Connexion().connect(sqlalchemy_engine=True)

    def find_a_customer(self, customer_id):
        query = f"SELECT customer.ID_CLIENT, DATE_ENTREE, NOM, PAYS, SEXE, AGE,\
             MEMBRE_ACTIF, BALANCE, NB_PRODUITS, CARTE_CREDIT, \
                SALAIRE, SCORE_CREDIT, CHURN\
                FROM customer\
                INNER JOIN indicators ON \
                    customer.ID_CLIENT=indicators.ID_CLIENT\
                WHERE customer.ID_CLIENT = {customer_id};"
        raw_customer = pd.read_sql(query, self.engine)
        raw_customer.columns = raw_customer.columns.str.upper()
        return raw_customer

    def load_all_customer_raw(self):
        query = "SELECT customer.ID_CLIENT, DATE_ENTREE, NOM, PAYS, SEXE, AGE,\
             MEMBRE_ACTIF, BALANCE, NB_PRODUITS, CARTE_CREDIT, \
                SALAIRE, SCORE_CREDIT, CHURN\
                FROM customer\
                INNER JOIN indicators ON \
                    customer.ID_CLIENT=indicators.ID_CLIENT;"
        data = pd.read_sql(query, self.engine)
        return data

    def load_all_ID(self):
        query="SELECT customer.ID_CLIENT FROM customer;"
        data = pd.read_sql(query, self.engine)
        data = data["id_client"].tolist()
        return data
    
#c =  CustomerLoader()
#cc = c.load_all_ID()
#print(cc)
#print(15686780 in cc)