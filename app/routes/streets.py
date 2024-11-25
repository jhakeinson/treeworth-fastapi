from statistics import mean
from fastapi import APIRouter
from sqlmodel import select
from app.lib.db.database import DBSessionDep
from app.lib.db.models.property import Street
from app.lib.utils.convert_to_float import convert_to_float

router = APIRouter(
    prefix="/streets",
    tags=["streets"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_streets(session: DBSessionDep):
    streets = session.exec(select(Street)).all()
    # filter out streets with no properties
    streets = [street for street in streets if street.properties]
    return [
        {
            **street.model_dump(),
            "average_price": mean([property.price for property in street.properties])
        }
        for street in streets
    ]