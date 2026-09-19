from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


# Pydantic models
class ItemCreate(BaseModel):
    name: str
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


class ItemPublic(BaseModel):
    id: int
    name: str
    price: float


class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    distance_to_center_km: float


class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"


app = FastAPI()


# In-memory data storage
_items: list[ItemPublic] = []
_next_id = 1


def _find(item_id: int) -> ItemPublic | None:
    """Find an item by its ID."""
    return next((item for item in _items if item.id == item_id), None)


def _has_same_name(name: str, item_id: int | None = None) -> bool:
    """Check for a duplicate name, ignoring letter case."""
    normalized_name = name.casefold()
    return any(
        item.name.casefold() == normalized_name and item.id != item_id
        for item in _items
    )


# Item APIs
# This fixed route must be declared before /items/{item_id}.
@app.get("/items/me", response_model=str)
def get_current_user_message() -> str:
    return "Welcome!"


@app.get("/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int) -> ItemPublic:
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items", response_model=ItemListResponse)
def get_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    q: str | None = Query(default=None, min_length=2),
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: Literal["id", "name", "price"] = "id",
    order: Literal["asc", "desc"] = "asc",
) -> ItemListResponse:
    filtered_items = list(_items)

    if q is not None:
        normalized_query = q.casefold()
        filtered_items = [
            item for item in filtered_items if normalized_query in item.name.casefold()
        ]

    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]

    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]

    total = len(filtered_items)
    reverse = order == "desc"

    if sort_by == "name":
        filtered_items.sort(key=lambda item: item.name.casefold(), reverse=reverse)
    elif sort_by == "price":
        filtered_items.sort(key=lambda item: item.price, reverse=reverse)
    else:
        filtered_items.sort(key=lambda item: item.id, reverse=reverse)

    paginated_items = filtered_items[skip : skip + limit]
    return ItemListResponse(
        items=paginated_items,
        total=total,
        skip=skip,
        limit=limit,
    )


@app.post("/items", response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> ItemPublic:
    global _next_id

    if _has_same_name(payload.name):
        raise HTTPException(
            status_code=409,
            detail="Item with this name already exists",
        )

    item = ItemPublic(id=_next_id, name=payload.name, price=payload.price)
    _items.append(item)
    _next_id += 1
    return item


@app.put("/items/{item_id}", response_model=ItemPublic)
def replace_item(item_id: int, payload: ItemCreate) -> ItemPublic:
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if _has_same_name(payload.name, item_id=item_id):
        raise HTTPException(
            status_code=409,
            detail="Item with this name already exists",
        )

    item.name = payload.name
    item.price = payload.price
    return item


@app.patch("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, payload: ItemUpdate) -> ItemPublic:
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    changes = payload.model_dump(exclude_unset=True)

    if "name" in changes:
        new_name = changes["name"]
        if new_name is None:
            raise HTTPException(status_code=422, detail="Name cannot be null")
        if _has_same_name(new_name, item_id=item_id):
            raise HTTPException(
                status_code=409,
                detail="Item with this name already exists",
            )

    if "price" in changes and changes["price"] is None:
        raise HTTPException(status_code=422, detail="Price cannot be null")

    if "name" in changes:
        item.name = changes["name"]
    if "price" in changes:
        item.price = changes["price"]

    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> Response:
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    _items.remove(item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# House price prediction API
@app.post("/predict/house-price", response_model=HousePricePrediction)
def predict_house_price(payload: HousePriceRequest) -> HousePricePrediction:
    predicted_price = (
        payload.area_sqm * 15_000_000
        - payload.distance_to_center_km * 5_000_000
        + payload.bedrooms * 20_000_000
    )
    return HousePricePrediction(predicted_price=predicted_price)


# Serve the frontend at /static/ after all API routes are defined.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="static",
)
