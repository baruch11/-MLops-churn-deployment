import pandas as pd
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
    
    def does_the_ID_exist(self, customer_id):
        query = f"SELECT CASE \
             WHEN EXISTS(SELECT ID_CLIENT FROM customer WHERE ID_CLIENT = {customer_id}) \
                        THEN  'Client ID exists'\
                        ELSE  'Client ID does not exist' \
                        END AS result;"
        result_query= pd.read_sql(query, self.engine)
        result_=result_query['result'].values.tolist()[0]
        if result_ == "Client ID exists":
            result_ = True
        else:
            result_ = False
        return result_ 