import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TransformEngine:
    @staticmethod
    def clean_data(raw_data):
        if not raw_data:
            logger.warning("No data provided to TransformEngine.")
            return None
            
        try:
            logger.info(f"Transforming {len(raw_data)} raw records.")
            df = pd.DataFrame(raw_data)
        
            # 1. Standardization: Lowercase columns for SQL compatibility
            df.columns = [col.lower() for col in df.columns]
        
            # 2. Data Cleaning: Rounding geographical decimals
            if 'rhaarea' in df.columns:
                df['rhaarea'] = df['rhaarea'].round(2)
            if 'landarea' in df.columns:
                df['landarea'] = df['landarea'].round(2)
        
            # 3. Feature Engineering: Calculating Water Area
            
            if 'rhaarea' in df.columns and 'landarea' in df.columns:
                df['water_area'] = (df['rhaarea'] - df['landarea']).round(2)
                logger.info("Feature engineering: water_area calculated.")
        
            if 'rhaname' in df.columns:
                df['rhaname'] = df['rhaname'].str.strip()
            

            columns_to_keep = ['objectid', 'rhacode', 'rhaname', 'rhaarea', 'landarea', 'water_area']
            df = df[columns_to_keep]

            logger.info("Transformation successful: DataFrame validated.")
        
            return df

        except Exception as e:
            logger.error(f"Error during data transformation: {e}")
            return None