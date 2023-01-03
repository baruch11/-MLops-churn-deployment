import pandas as pd

from chaos.infrastructure.connexion import Connexion


class SocioEco:
    TABLE = "socio_eco"

    def __init__(self):
        self.engine = Connexion().connect()

    def read(self) -> pd.DataFrame:
        """Returns socio eco data"""
        query = f"SELECT * FROM {self.TABLE}"
        data = pd.read_sql(query, self.engine)
        return data
