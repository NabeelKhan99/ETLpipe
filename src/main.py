from ingest import IngestEngine
from transform import TransformEngine
from load import LoadEngine

def run_pipeline():
    """
    Orchestrates the ETL process for Manitoba Health RHA data.
    Separates concerns between Ingestion, Transformation, and Loading.
    """
    print("Initializing ETL Pipeline...")
    
    # Phase 1: Ingestion
    # Responsible for API communication and raw data retrieval
    ingestor = IngestEngine()
    raw_data = ingestor.fetch_rha_data()
    
    if not raw_data:
        print("Error: No data retrieved during Ingestion phase.")
        return

    print(f"Ingestion Phase Complete: {len(raw_data)} records retrieved.")

    # Phase 2: Transformation
    # Responsible for data cleaning, type casting, and feature engineering
    transformer = TransformEngine()
    processed_df = transformer.clean_data(raw_data)
    
    if processed_df is None or processed_df.empty:
        print("Error: Data transformation returned an empty dataset.")
        return

    print("Transformation Phase Complete: Data standardized and features engineered.")

    # Phase 3: Loading
    # Responsible for persistence to the database layer
    loader = LoadEngine()
    load_success = loader.save_to_sql(processed_df)
    
    if load_success:
        print("Load Phase Complete: Data successfully persisted to destination.")
        print("Pipeline Execution Summary: Success")
    else:
        print("Pipeline Execution Summary: Failed during Load Phase")

if __name__ == "__main__":
    run_pipeline()