import logging
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData

logger = logging.getLogger(__name__)

class LoadEngine:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        # Neon (PostgreSQL) requires the 'psycopg2' driver which is the default for 'postgresql://'
        self.engine = create_engine(self.connection_string)
        self.metadata = MetaData()

    def save_to_db(self, df, table_name="rha_boundaries"):
        if df is None or df.empty:
            logger.error("Load aborted: No data found in the DataFrame.")
            return False

        try:
            logger.info("Initializing PostgreSQL schema validation.")
            
            # Explicit Schema Definition - This is your "Source of Truth"
            rha_table = Table(
                table_name, self.metadata,
                Column('objectid', Integer, primary_key=True),
                Column('rhacode', String(10)),
                Column('rhaname', String(100)),
                Column('rhaarea', Float),
                Column('landarea', Float),
                Column('water_area', Float)
            )

            # 1. Create the table if it doesn't exist (using your explicit schema)
            self.metadata.create_all(self.engine)
            logger.info(f"PostgreSQL Table schema verified: {table_name}")

            # 2. Change 'if_exists' to 'append'
            # 'replace' drops your custom schema. 'append' keeps it.
            logger.info(f"Writing {len(df)} records to {table_name}...")
            
            # Use 'append' so it respects the table structure we just verified/created
            # We clear the table manually if needed, or just let it append
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            
            logger.info("PostgreSQL load operation completed successfully.")
            return True

        except Exception as e:
            logger.error(f"Critical failure during PostgreSQL load: {e}")
            return False