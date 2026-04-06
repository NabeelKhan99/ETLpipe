import logging
from ingest import IngestEngine
from transform import TransformEngine
from load import LoadEngine

# Centralized Logging Configuration
# This ensures all modules reporting to 'ETL_Orchestrator' use the same format and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ETL_Orchestrator")

def run_pipeline():
    """
    Main entry point for the ETL Pipeline.
    Manages the flow between Ingest, Transform, and Load engines.
    """
    logger.info("Initializing ETL Pipeline execution.")
    
    # Phase 1: Ingestion
    try:
        ingestor = IngestEngine()
        raw_data = ingestor.fetch_rha_data()
        
        if not raw_data:
            logger.error("Pipeline aborted: Ingestion engine returned no data.")
            return
            
        logger.info(f"Ingestion successful: {len(raw_data)} records retrieved.")
    except Exception as e:
        logger.critical(f"Critical failure in Ingestion phase: {e}")
        return

    # Phase 2: Transformation
    try:
        # Note: Calling as a static method if defined as @staticmethod in transform.py
        processed_df = TransformEngine.clean_data(raw_data)
        
        if processed_df is None or processed_df.empty:
            logger.error("Pipeline aborted: Transformation engine returned empty DataFrame.")
            return

        logger.info("Transformation successful: Data standardized and validated.")
    except Exception as e:
        logger.error(f"Failure in Transformation phase: {e}")
        return

    # Phase 3: Loading
    try:
        loader = LoadEngine()
        load_success = loader.save_to_sql(processed_df)
        
        if load_success:
            logger.info("Load successful: Data persisted to destination database.")
            logger.info("ETL Pipeline Execution: SUCCESS")
        else:
            logger.warning("Load failed: Database write was unsuccessful.")
    except Exception as e:
        logger.error(f"Failure in Load phase: {e}")

if __name__ == "__main__":
    run_pipeline()