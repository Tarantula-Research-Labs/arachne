from connection import Connection
from fastapi import FastAPI, Body
from order_execution import VerificationChecks, place_single_order, exit_position
import boto3
# from order_execution import view_funds, VerificationChecks

app = FastAPI()
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

@app.get("/exit-all-positions")
async def exit_all_positions():
    conn = Connection()
    return exit_position(conn)

@app.post("/update-token")
def update_token(token: str):
    ssm.put_parameter(
        Name=PARAM_NAME,
        Value=token,
        Type="SecureString",
        Overwrite=True
    )
    return {"message": "Token updated"}

@app.get("/token")
def get_token():
    response = ssm.get_parameter(
        Name=PARAM_NAME,
        WithDecryption=True
    )
    return {"token": response["Parameter"]["Value"]}


# if __name__ == "__main__":
#     print("test")
#     conn = Connection()
#     print(view_funds(conn))
#     vc = VerificationChecks("TMPV")
#     print(vc.active_position())

