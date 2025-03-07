from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from datetime import datetime
import math
from enum import Enum

STAMP_DUTY_THRESHOLD = 150
STAMP_DUTY = 10
SST_RATE = 0.06

PRICING_TABLE = {
    "area1": {
        "plan1": [30, 44, 59, 69, 19],
        "plan2": [45, 65, 89, 103, 29],
        "plan3": [55, 80, 110, 125, 50],
    },
    "area2": {
        "plan1": [43, 70, 107, 126, 34],
        "plan2": [65, 105, 161, 189, 50],
        "plan3": [75, 122, 187, 219, 59],
    },
}

COVID_ADDON_TABLE = {
    "area1": {
        "plan1": [12, 24, 33, 55, 12],
        "plan2": [27, 36, 45, 68, 24],
        "plan3": [39, 43, 58, 97, 38],
    },
    "area2": {
        "plan1": [23, 33, 54, 85, 23],
        "plan2": [36, 50, 78, 120, 35],
        "plan3": [59, 79, 118, 117, 56],
    },
}

app = FastAPI()


class Area(str, Enum):
    AREA1 = "area1"
    AREA2 = "area2"


class Plan(str, Enum):
    PLAN1 = "plan1"
    PLAN2 = "plan2"
    PLAN3 = "plan3"


class PriceResponse(BaseModel):
    base_price: int
    covid_addon: int
    stamp_duty: int
    sst: float
    total_price: float


def calculate_price_from_table(table: dict, area: str, plan: str, duration: int) -> int:
    pricing = table[area][plan]
    if duration <= 5:
        return pricing[0]
    elif duration <= 10:
        return pricing[1]
    elif duration <= 18:
        return pricing[2]
    elif duration <= 31:
        return pricing[3]
    else:
        extra_weeks = math.ceil((duration - 31) / 7)
        return pricing[3] + (extra_weeks * pricing[4])


@app.get("/calculate", response_model=PriceResponse)
async def calculate_price(
    area: Area = Query(default=Area.AREA1, description="The coverage area"),
    plan: Plan = Query(default=Plan.PLAN1, description="The insurance plan"),
    departure_date: str = Query(
        default=datetime.now().strftime("%Y-%m-%d"),
        description="Departure date in YYYY-MM-DD format",
    ),
    return_date: str = Query(
        default=datetime.now().strftime("%Y-%m-%d"),
        description="Return date in YYYY-MM-DD format",
    ),
    covid_addon: bool = Query(default=False, description="Include COVID-19 coverage"),
):
    """Calculate the total insurance price based on area, plan, travel duration, and optional COVID-19 coverage."""
    try:
        departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
        return_date = datetime.strptime(return_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
        )

    duration = (return_date - departure_date).days + 1
    if duration <= 0:
        raise HTTPException(
            status_code=400, detail="Return date must be after departure date"
        )

    base_price = calculate_price_from_table(PRICING_TABLE, area, plan, duration)
    covid_price = (
        calculate_price_from_table(COVID_ADDON_TABLE, area, plan, duration)
        if covid_addon
        else 0
    )
    total_price = base_price + covid_price

    stamp_duty = STAMP_DUTY if total_price >= STAMP_DUTY_THRESHOLD else 0
    total_price += stamp_duty

    sst = round(total_price * SST_RATE, 2) if area == Area.AREA1 else 0
    total_price += sst

    return PriceResponse(
        base_price=base_price,
        covid_addon=covid_price,
        stamp_duty=stamp_duty,
        sst=sst,
        total_price=total_price,
    )
