from fastapi import APIRouter

router = APIRouter(
    prefix="/streets",
    tags=["streets"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_streets():
    return {"message": "Hello World"}