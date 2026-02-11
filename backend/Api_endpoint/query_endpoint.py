from backend.graph.app import AgentGraph
from fastapi import APIRouter,HTTPException
from backend.schema.response_models import QueryResponse,UploadResponse,QueryRequest

router = APIRouter()

workflow = AgentGraph().final_workflow()


@router.post("/query",response_model=QueryResponse)
def user_query(req: QueryRequest):

    try:

        output = workflow.invoke(req.model_dump())

        if not output:
            raise ValueError("Empty workflow response")
        
        return {"status":"success","messages": output}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






