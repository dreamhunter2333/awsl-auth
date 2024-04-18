from fastapi import APIRouter, status

router = APIRouter()


@router.get("/api/health_check", tags=["health check"])
def health_check():
    return status.HTTP_200_OK
