import pandas as pd
import webbrowser
from fyers_apiv3 import fyersModel
from datetime import datetime, timedelta
import time
import boto3
from connection import Connection


client_id="W7LM9VJA41-200"
secret_key="qpKCdzLr6qijQPIR"
redirect_uri="https://tarantularesearch.com/"

ssm = boto3.client("ssm", region_name="ap-south-1")
PARAM_NAME = "/trading/access_token"

def get_access_token():
    ssm = boto3.client("ssm", region_name="ap-south-1")
    response = ssm.get_parameter(
        Name=PARAM_NAME,
        WithDecryption=True
    )
    return response["Parameter"]["Value"]


def send_historical_data(connection):
    conn = connection
    fyers = fyersModel.FyersModel(client_id=conn.get("client_id"), token=get_access_token(), is_async=False, log_path="")

    data = {
    "symbol":"NSE:TMPV-EQ",
    "resolution":"D",
    "date_format":"1",
    "range_from":(datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
    "range_to":datetime.now().strftime("%Y-%m-%d"),
    "cont_flag":"1"
    }
    datetime.now().strftime("%d%m%Y")
    response = fyers.history(data=data)
    # print(response)

    df = pd.DataFrame(
        response["candles"],
        columns=["timestamp", "open", "high", "low", "close", "volume"],
    )
    df["timestamp"] = (
        pd.to_datetime(df["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
    )
    df = df.set_index("timestamp")
    print(df)
    return df
