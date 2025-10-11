from typing import List
from fastapi import APIRouter
from model.category import Category

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/category", response_model=List[Category])
async def get_category() -> List[Category]:
    return [Category.family, Category.career, Category.society]
