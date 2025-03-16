from fastapi import APIRouter, Request
import app
from app.gmail_api.functions import get_google_access


router = APIRouter(tags=["DevelopeOnly"])


@router.get("/google_access")
def apiaccessRequest(code: str = None):
    try:
        app.state.google_token = get_google_access(code)

    except Exception as e:
        return "Failed to get a token: " + str(e)
