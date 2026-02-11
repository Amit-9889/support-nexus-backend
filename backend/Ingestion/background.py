from backend.Ingestion.load import data_loader
import logging


logger = logging.getLogger(__name__)

class background:

    def ingest_pdf(self,path:str):
        try:
            logger.info(f"Starting ingestion: {path}")
            data_loader(path=path).load()
            logger.info(f"Completed ingestion: {path}")

        except Exception:
            logger.error("Ingestion failed" , exc_info = True)