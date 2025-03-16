from urllib.parse import unquote
from fastapi import APIRouter, Request
from app.gmail_api.functions import get_google_access


router = APIRouter(tags=["DevelopeOnly"])


@router.get("/google_access")
def google_request_api(request: Request, code: str = None):
    try:
        if not code:
            return get_google_access()
        else:
            response = get_google_access(unquote(code))
            request.app.state.google_token = get_google_access(unquote(code))
            return {"status": 200, "data": response}

    except Exception as e:
        return "Failed to get a token: " + str(e)
