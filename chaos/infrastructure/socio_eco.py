import pandas as pd

from chaos.infrastructure.connexion import Connexion


engine = Connexion().connect()


class SocioEco:
    TABLE = "socio_eco"

    @classmethod
    def read(cls) -> pd.DataFrame:
        """Returns socio eco data"""
        query = f"SELECT * FROM {cls.TABLE}"
        data = pd.read_sql(query, engine)
        return data
