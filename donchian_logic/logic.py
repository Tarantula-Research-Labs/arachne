import pandas as pd
import requests
from connection import Connection
from order_execution import VerificationChecks
from datetime import datetime, timedelta
from fyers_apiv3 import fyersModel
import time
import pytz





def fyers_history_to_df(response: dict, resolution: int) -> pd.DataFrame:
    """
    Convert FYERS history API response to a pandas DataFrame.
    Shifts intraday candle timestamps forward by `resolution` minutes
    to convert open-time to close-time.
    """

    if response.get("s") != "ok":
        raise ValueError(f"FYERS API error: {response}")

    df = pd.DataFrame(
        response["candles"],
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    # Convert UNIX epoch → timezone-aware datetime (IST)
    df["datetime"] = (
        pd.to_datetime(df["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
    )

    # Shift candle open-time → close-time
    df["datetime"] = df["datetime"] + pd.Timedelta(minutes=resolution)

    df = df.sort_values("datetime")
    df = df.drop(columns=["timestamp"])

    return df

class DonchianLogic:
    def __init__(self, ticker, conn):
        self.ticker = f"NSE:{ticker.upper()}-EQ"
        self.client_id = conn.get("client_id")
        self.access_token = conn.get("access_token")
        self.start_date = None
        self.end_date = None

    def fetch_past_bars(self):
        print(datetime.today()-timedelta(2))
        print(datetime.today())
        print(datetime.now().strftime("%A"))
        print(datetime.now().strftime("%Y-%m-%d"))
        self.end_date = datetime.now().strftime("%Y-%m-%d")
        self.start_date = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
        print("Start Date", self.start_date)
        print("End Date", self.end_date)

    def combined_data_function(self, resolution, start_date, end_date):
        fyers = fyersModel.FyersModel(client_id=self.client_id, is_async=False, token=self.access_token, log_path="")

        data = {
            "symbol": self.ticker,
            "resolution": resolution,
            "date_format": "1",
            "range_from": start_date,
            "range_to": end_date,
            "cont_flag": "1",
            "oi_flag": 1
        }

        response = fyers.history(data=data)
        df = fyers_history_to_df(response, resolution=resolution)  # pass resolution explicitly
        df = df.set_index("datetime")
        # df.to_excel("test.xlsx")

        return df


if __name__ == "__main__":

    for i in range(360):
        start_time = time.time()
        # connect = Connection()
        # dc = DonchianLogic("TMPV", connect)
        # dc.fetch_past_bars()
        # print(dc.combined_data_function(resolution = 5,start_date=dc.start_date, end_date=dc.end_date))
        ist = pytz.timezone("Asia/Kolkata")
        print(datetime.now(ist).strftime("%H-%M-%S"))
        print("Elapsed Time", time.time() - start_time)

        time.sleep(5)



