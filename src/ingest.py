import requests
import logging

logger = logging.getLogger(__name__)

class IngestEngine:
    def __init__(self):
        self.api_url = "https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/Manitoba_Regional_Health_Authorities/FeatureServer/0/query"

    def fetch_rha_data(self):
        params = {
            "where": "1=1",
            "outFields": "*",
            "f": "json",
            "returnGeometry": "false"
        }
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status() 

            data = response.json()

            if "error" in data:
                logger.error(f"ArcGIS Server Error: {data['error'].get('message')}")
                return []
            
            features = data.get("features", [])


            if features:
                logger.info(f"Successfully retrieved {len(features)} records.")
                # Extracting only the attributes dictionary for each record
                return [f['attributes'] for f in features]
            
            logger.warning("API connection successful but no records were returned.")
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"Network or Connection Error during ingestion: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in IngestEngine: {e}")
            return []
        
        