from fastapi import APIRouter, Depends
from ikea_recommender.app.domains.recommender.services import RecommenderService
from ikea_recommender.app.api.dependencies import get_recommender_service

router = APIRouter(prefix="/recommend", tags=["recommendation"])

@router.get("/by-text")
async def recommend_by_text(query: str, top_k: int = 10, service: RecommenderService = Depends(get_recommender_service)):
    return service.recommend_by_text(query, top_k)

@router.get("/by-id/{product_id}")
async def recommend_by_id(product_id: str, top_k: int = 10, service: RecommenderService = Depends(get_recommender_service)):
    return service.recommend_by_id(product_id, top_k)
