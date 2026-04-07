from fyers_apiv3 import fyersModel
from connection import Connection

class VerificationChecks:

    def __init__(self, ticker):
        self.conn = Connection()
        self.fyers = fyersModel.FyersModel(client_id=self.conn.get("client_id"), token=self.conn.get("access_token"), is_async=False, log_path="")
        self.ticker = f"NSE:{ticker.upper()}-EQ"

    def active_position(self):
        response = self.fyers.positions()
        status = response["overall"] #This tells the number of active positions, not which one is active. So for the first iteration, we will only focus on number of active position
        return status["count_open"] == 1

    def calculate_shares(self):
        data = {
            "symbols": self.ticker
        }
        response = self.fyers.quotes(data=data)
        last_traded_price = response["d"][0]["v"]["lp"]
        capital = self.conn.get("capital")
        number_of_shares = int(round(capital/last_traded_price,0))

        return {"last_traded_price": last_traded_price, "capital": capital, "shares": number_of_shares}
