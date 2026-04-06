import pandas as pd

class TransformEngine:
    @staticmethod
    def clean_data(raw_data):
        if not raw_data:
            return None
            
        df = pd.DataFrame(raw_data)
        
        # 1. Standardization: Lowercase columns for SQL compatibility
        df.columns = [col.lower() for col in df.columns]
        
        # 2. Data Cleaning: Rounding geographical decimals
        df['rhaarea'] = df['rhaarea'].round(2)
        df['landarea'] = df['landarea'].round(2)
        
        # 3. Feature Engineering: Calculating Water Area
        df['water_area'] = (df['rhaarea'] - df['landarea']).round(2)
        
        return df