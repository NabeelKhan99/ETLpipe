import sqlite3
import pandas as pd

class LoadEngine:
    def __init__(self, db_name="manitoba_health.db"):
        self.db_name = db_name

    def save_to_sql(self, df, table_name="rha_boundaries"):
        try:
            print(f" Phase 3: Loading data into {self.db_name}...")
            # Create a connection to the SQLite database
            with sqlite3.connect(self.db_name) as conn:
                # if_exists='replace' ensures we don't get duplicate errors during testing
                df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            print(f" Load Complete: Table '{table_name}' is ready.")
            return True
        except Exception as e:
            print(f" Load Error: {e}")
            return False