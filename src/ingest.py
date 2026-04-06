import requests

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
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            # Return only the raw attributes list
            return [feature['attributes'] for feature in data.get('features', [])]
        except Exception as e:
            print(f"Ingestion Error: {e}")
            return []