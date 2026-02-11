from fastapi import APIRouter,UploadFile,File, HTTPException, BackgroundTasks
from backend.Ingestion.background import background
from backend.schema.response_models import UploadResponse
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload",response_model=UploadResponse)
async def upload_file(file:UploadFile = File(...),
                      background_tasks: BackgroundTasks = None):

        if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="Only PDF files allowed")
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        ## Save pdf

        try:
            with open(file_path,"wb") as f:
                f.write(await file.read())

                ## Calling data_loader object
                
            background_tasks.add_task(background().ingest_pdf,file_path)

            return {"status":"success","messages":"File uploaded . Ingestion started in background."}
        

        except Exception as e:
              raise HTTPException(status_code=500 , details=str(e))

