import pandas as pd
from chaos.infrastructure.connexion import Connexion

class NoSQL_access(Exception):
    """Postgres instance not found."""

class CustomerLoader:

    def __init__(self):
        self.engine = Connexion().connect(sqlalchemy_engine=True)

    def find_a_customer(self, customer_id):
        """Query the database to find a customer

        Parameters
        ----------
        customer_id : int
                      client ID

        Returns
        -------
        raw_customer : pd.Dataframe
                       customer's features 

        """
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
        """Query the database to load complete data"""

        query = "SELECT customer.ID_CLIENT, DATE_ENTREE, NOM, PAYS, SEXE, AGE,\
             MEMBRE_ACTIF, BALANCE, NB_PRODUITS, CARTE_CREDIT, \
                SALAIRE, SCORE_CREDIT, CHURN\
                FROM customer\
                INNER JOIN indicators ON \
                    customer.ID_CLIENT=indicators.ID_CLIENT;"
        data = pd.read_sql(query, self.engine)
        return data
    
    def does_the_ID_exist(self, customer_id):
        """Query the database to find out if the id exists

        Parameters
        ----------
        customer_id : int
                      client ID
        Returns
        -------
        result_ : boolean

        """
        query = f"SELECT CASE \
             WHEN EXISTS(SELECT ID_CLIENT FROM customer WHERE ID_CLIENT = {customer_id}) \
                        THEN  'Client ID exists'\
                        ELSE  'Client ID does not exist' \
                        END AS result;"
        result_query= pd.read_sql(query, self.engine)
        result_=result_query['result'].values.tolist()[0]
        return result_ == "Client ID exists"
