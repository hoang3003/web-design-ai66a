from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


def predict_price(area: float, bedrooms: int, location: str) -> float:
    total = 500_000_000
    total += area * 15_000_000
    total += bedrooms * 50_000_000

    normalized_location = location.lower()
    if normalized_location == "hanoi":
        total *= 1.3
    elif normalized_location == "hcmc":
        total *= 1.25

    return float(round(total / 1_000_000) * 1_000_000)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


# This uses def because the calculation is CPU-only and does not await any I/O.
@app.get("/predict")
def get_prediction(area: float, bedrooms: int, location: str = "other"):
    predicted_price = predict_price(area, bedrooms, location)

    return {
        "area": area,
        "bedrooms": bedrooms,
        "location": location,
        "predicted_price": predicted_price,
    }
