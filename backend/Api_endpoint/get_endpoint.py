from fastapi import APIRouter



router = APIRouter()
## Get endpoint

@router.get('/health')
def health():
    return {"status":"ok"}


    




