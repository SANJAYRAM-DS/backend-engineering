from fastapi import APIRouter, Depends, status
from src.schemas.url import URLCreateRequest, URLResponse, AnalyticsResponse
from src.services.url_service import URLService
from src.api.deps import get_url_service

router = APIRouter(prefix="/urls", tags=["URLs"])


@router.post("", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    request: URLCreateRequest,
    url_service: URLService = Depends(get_url_service),
):
    return await url_service.create_short_url(request)


@router.get("/{short_code}/analytics", response_model=AnalyticsResponse)
async def get_analytics(
    short_code: str,
    url_service: URLService = Depends(get_url_service),
):
    return await url_service.get_analytics(short_code)


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    short_code: str,
    url_service: URLService = Depends(get_url_service),
):
    await url_service.delete_url(short_code)
    return None