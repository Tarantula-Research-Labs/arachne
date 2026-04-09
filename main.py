from connection import Connection
from fastapi import FastAPI
from order_execution import VerificationChecks, place_single_order, exit_position
from authentication import update_access_token

ticker = "TMPV"
app = FastAPI()
# conn = Connection()

@app.get("/")
async def root():
    return {"Welcome to Arachne, A property of Tarantula Research Labs"}

@app.get("/place-order")
async def orders():
    vc = VerificationChecks(ticker)
    conn = Connection()
    if vc.active_position():
        return {"Message": "A position is already active, cannot place new order"}
    else:
        shares = vc.calculate_shares()["shares"]
        return place_single_order(conn, ticker, shares)

@app.get("/update_config/{access_token}")
async def config_update(access_token):
    data = update_access_token(access_token)
    return data

@app.get("/exit-all-positions")
async def exit_all_positions():
    conn = Connection()
    return exit_position(conn)


# if __name__ == "__main__":
#     print("test")
#     print(view_funds(conn))

