import json
from fastapi import APIRouter
from authentication import TokenCreation
from metrics import send_historical_data
from connection import Connection
router = APIRouter()

tc = TokenCreation()

@router.get("/create_token_url", tags=["daily authentication"])
async def create_token():
    auth_url = tc.generate_auth_token()
    return auth_url

@router.get("/create_and_save_access_token/{rawtoken:path}", tags=["daily authentication"])
async def create_access_token(rawtoken: str):
    conn = Connection()
    access_token = tc.generate_access_token(rawtoken)
    print(access_token)
    historical_data = send_historical_data(conn)
    return {
        "access_token": access_token,
        "historical_data": json.loads(
            historical_data.reset_index().to_json(orient="records", date_format="iso")
        ),
    }
