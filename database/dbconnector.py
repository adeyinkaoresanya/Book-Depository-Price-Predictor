import pandas as pd
from sqlalchemy import create_engine,  exc
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser


class DatabaseError(exc.SQLAlchemyError):
    pass

class DatabaseConnector:
    """
    Database class. Handles all connections to the database on heroku.
    """
    
    def read_config(self):
        config = configparser.ConfigParser()
        config.read("configfile/config_file.ini")
        db_param = config["postgresql"]
        user = db_param["user"]
        password = db_param["password"]
        host = db_param["host"]
        port = int(db_param["port"])
        database = db_param["database"]
        db_host = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return db_host
 
    def connect_engine(self):
        """
        This function create a database engine for connecting to database 

        """
        try:
            db_host = self.read_config()
            engine = create_engine(db_host, echo= False)
            db = scoped_session(sessionmaker(bind=engine))
            return db
        except DatabaseError:
            raise DatabaseError("Error connecting to the database")
            #db.rollback()

    def create_table(self) -> None:
        """
        Sets up table for tracking predictions in the database    
        Returns:
            None
        """
        db = self.connect_engine()
        try:
            db.execute("""CREATE TABLE IF NOT EXISTS bookpredictions(id SERIAL PRIMARY KEY, genre VARCHAR,
                    format VARCHAR,  number_of_pages INT, weight FLOAT, rating FLOAT, rating_count FLOAT,
                    year INT, outputs FLOAT)""")
            db.commit()
            print("bookpredictions table is now in the database.")
        except (DatabaseError, Exception) as error:
                raise error("Could not create table in the database.")
                db.rollback()

    def delete_table(self) -> None:
        """
        deletes table for tracking predictions in the database    
        Returns:
            None
        """
        db = self.connect_engine()
        try:
            db.execute("DROP TABLE IF EXISTS bookpredictions")
            print("BookPredictions table  is no longer in the database.")
        except (Exception, DatabaseError) as error:
            raise error("Something went wrong while carrying out this request")
            db.rollback()

    def save_predictions_to_database(self, df: pd.DataFrame, file_title: str) -> None:
        """
        Adds the features and predictions to a table in the database

        Args:
            df (pd.DataFrame): the table to be stored in the database
            file_title (str): title of the output file

        Returns:
            None   
        """
        db_host = self.read_config()
        db = self.connect_engine()
        engine = create_engine(db_host, echo= False)
        try:
            df.to_sql(f'{file_title}', engine, if_exists= "append", index= False)
           # db.commit()
            db.close()
        except (DatabaseError, Exception) as error:
            raise error("Error occurred when trying to add predictions to the database")
            db.rollback()


    def pull_predictions_from_database(self) -> list:
        """
        pulls the lastest 10 predictions from the database
        
        Returns:
            List of tuples containing the lastest 10 predictions   
            
        """
        results = []
        db = self.connect_engine()
        try:
            query= "SELECT * FROM bookpredictions ORDER BY id DESC LIMIT 10"
            query_df = db.execute(query)
            rows= query_df.fetchall()
            columns = db.execute(query).keys()
            for row in rows:
                results.append(dict(zip(columns, list(row))))
            return results
            db.close()
        except (DatabaseError, Exception) as error:
            raise error("Error occurred when trying to pull predictions from the database")
            db.rollback()


