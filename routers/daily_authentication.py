from fastapi import APIRouter
from authentication import TokenCreation
router = APIRouter()

tc = TokenCreation()

@router.get("/create_token_url", tags=["daily authentication"])
async def create_token():
    auth_url = tc.generate_auth_token()
    return auth_url

@router.get("/create_and_save_access_token/{rawtoken:path}", tags=["daily authentication"])
async def create_access_token(rawtoken: str):
    access_token = tc.generate_access_token(rawtoken)
    return access_token
