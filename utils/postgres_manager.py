import logging, argparse
from sqlalchemy import create_engine
from chaos.infrastructure.config.config import config
from sqlalchemy.types import Integer, Text, String, Date
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--customer",
                    help="Provide your personal test sample customer.csv file\
                         to feed database ",
                    default="./chaos/test/data/test_sample_customer.csv")
parser.add_argument("-i", "--indicators",
                    help="Provide your personal test sample indicators.csv \
                    file to feed database ",
                    default="./chaos/test/data/test_sample_indicators.csv")
args = parser.parse_args()

if (args.indicators is None or args.customer is None):
    raise NameError("Please provide an indicators filename \
    or a customer filename, use --help for more information")


class PostgresManager:
    PATH_TO_INDICATORS_CSV = args.indicators
    PATH_TO_CUSTOMER_CSV = args.customer

    def __init__(self):

        """
        config_file : dict
            The YAML file describing the connexion configuration to postgresql
        """
        param = config["external_postgres"]
        self.username = param["username"]
        self.password = param["password"]
        self.hostname = param["hostname"]
        self.database = param["database"]
        self.port = param["port"]
        url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            self.username,
            self.password,
            self.hostname,
            self.port,
            self.database
        )
        self.engine = create_engine(url, isolation_level="AUTOCOMMIT")

    def initialize_data(self):
        self.delete_db()
        self.add_csv_data()
        logging.info("All your data uploaded well")

    def delete_db(self):
        """ In this function we can't re-use the self.engine object because we
        want to create another in order to connect to postgres (default)
        database, and from this one delete (if it exist) the db.
        """
        url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            self.username,
            self.password,
            self.hostname,
            self.port,
            "postgres"
        )
        engine = create_engine(url, isolation_level="AUTOCOMMIT")
        with engine.connect() as con:
            con.execute(f"DROP DATABASE IF EXISTS {self.database}")
            con.execute(f"CREATE DATABASE {self.database}")

    def add_csv_data(self):
        df_indicators = pd.read_csv(self.PATH_TO_INDICATORS_CSV)
        # We put index into lower case due to postgres syntax
        df_indicators.columns = df_indicators.columns.str.lower()
        df_indicators.to_sql('indicators',
                             self.engine,
                             if_exists='replace',
                             index=False)
        df_customer = pd.read_csv(
            self.PATH_TO_CUSTOMER_CSV,
            parse_dates=['DATE_ENTREE']
            )
        # We put index into lower case due to postgres syntax
        df_customer.columns = df_customer.columns.str.lower()
        df_customer.to_sql('customer',
                           self.engine,
                           if_exists='replace',
                           index=False)


if __name__ == '__main__':
    p_m = PostgresManager()
    p_m.initialize_data()
