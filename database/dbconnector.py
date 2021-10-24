import pandas as pd
from decouple import config
import psycopg2
import psycopg2.extras as extras


class DatabaseError(psycopg2.Error):
    pass

class DatabaseConnector:
    """
    Database class. Handles all connections to the database on Heroku.
    """
    connection = psycopg2.connect(
                                  dbname=config("database"),
                                  port=config("port"),
                                  host=config("host"),
                                  user=config("user"),
                                  password=config("password")
                                  )
    connection.autocommit = True
    cursor = connection.cursor()

    def connect(self) -> object:
        """
        Connects to the postgres database.
        
        return: database connection cursor
        """
        try:
            return self.cursor
        except DatabaseError:
            raise DatabaseError


   
    def create_table(self) -> None:
        """
        Sets up table for tracking predictions in the database    
        Returns:
            None
        """

        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS bookpredictions(id SERIAL PRIMARY KEY, genre VARCHAR,
                    format VARCHAR,  number_of_pages INT, weight FLOAT, rating FLOAT, rating_count FLOAT,
                    year INT, price FLOAT)""")
            print("bookpredictions table is now in the database.")
        except (DatabaseError, Exception) as error:
            raise error

    def delete_table(self) -> None:
        """
        deletes table for tracking predictions in the database    
        Returns:
            None
        """
        
        try:
            self.cursor.execute("DROP TABLE IF EXISTS bookpredictions")
            print("bookpredictions table is no longer in database.")
        except (Exception, DatabaseError) as error:
            raise error

    def save_predictions_to_database(self, df: pd.DataFrame) -> None:
        """
        Adds the features and predictions to a table in the database

        Args:
            df (pd.DataFrame): the table to be stored in the database

        Returns:
            None   
        """
        try:
            self.create_table()
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))
            query = "INSERT INTO %s(%s) VALUES(%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)" % ('bookpredictions', cols)
            extras.execute_batch(self.cursor, query, tuples, len(df))
            print("Record successfully added to bookpredictions")
        except (DatabaseError, Exception) as error:
            raise error

    def pull_predictions_from_database(self) -> list:
        """
        pulls the lastest 10 predictions from the database
        
        Returns:
            List of tuples containing the lastest 10 predictions   
            
        """
        try:
            self.cursor.execute("SELECT * FROM bookpredictions ORDER BY id DESC LIMIT 10")
            return self.cursor.fetchall()
        except Exception:
            raise Exception
