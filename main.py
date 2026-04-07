from connection import Connection
from fastapi import FastAPI
from order_execution import place_single_order
from authentication import update_access_token

app = FastAPI()
conn = Connection()

@app.get("/")
async def root():
    return {"Welcome to Arachne, A property of Tarantula Research Labs"}

@app.get("/place-order")
async def orders():
    conn = Connection()   # fresh config loaded
    return place_single_order(conn)

@app.get("/update_config/{access_token}")
async def config_update(access_token):
    data = update_access_token(access_token)
    return data