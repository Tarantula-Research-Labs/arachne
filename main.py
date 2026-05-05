from connection import Connection
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from order_execution import VerificationChecks, place_single_order, exit_position
import boto3
from routers import bot_controllers, daily_authentication
# from order_execution import view_funds, VerificationChecks

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                  # local dev
        "https://argus.tarantularesearch.com",   # replace with your actual frontend domain
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Bot Controller
app.include_router(bot_controllers.router)
#Daily Authentication
app.include_router(daily_authentication.router)


ssm = boto3.client("ssm", region_name="ap-south-1")
PARAM_NAME = "/trading/access_token"


@app.get("/")
async def root():
    return {"Welcome to Arachne, A property of Tarantula Research Labs"}

@app.post("/place-order")
async def orders(items: dict = Body(...)):
    ticker = items["ticker"]
    order_type = items["order_type"]
    vc = VerificationChecks(ticker)
    conn = Connection()
    if vc.active_position():
        return {"Message": "A position is already active, cannot place new order"}
    else:
        shares = vc.calculate_shares()["shares"]
        return place_single_order(conn, ticker, shares, order_type)

@app.post("/exit-all-positions")
async def exit_all_positions(items: dict = Body(...)):
    ticker = items["ticker"]
    numOfshares = items["numOfshares"]
    orderType = items["orderType"]
    ltp = items["ltp"]
    conn = Connection()
    return exit_position(conn, ticker, numOfshares, orderType, ltp)


# if __name__ == "__main__":
#     print("test")
#     conn = Connection()
#     print(view_funds(conn))
#     vc = VerificationChecks("TMPV")
#     print(vc.active_position())

