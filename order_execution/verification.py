from fyers_apiv3 import fyersModel
from connection import Connection
from order_execution.funds import view_funds
from authentication import get_access_token

class VerificationChecks:

    def __init__(self, ticker):
        self.conn = Connection()
        self.fyers = fyersModel.FyersModel(client_id=self.conn.get("client_id"), token=get_access_token(), is_async=False, log_path="")
        self.ticker = f"NSE:{ticker.upper()}-EQ"

    def active_position(self):
        response = self.fyers.positions()
        print("positions response:", response)
        if "overall" not in response:
            return False
        status = response["overall"]
        return status["count_open"] == 1

    def calculate_shares(self):

        data = {
            "symbols": self.ticker
        }
        response = self.fyers.quotes(data=data)
        last_traded_price = response["d"][0]["v"]["lp"]
        capital = view_funds(self.conn)
        capital_percentage = 0.7
        number_of_shares = int((capital*5*capital_percentage)/last_traded_price)
        return {"last_traded_price": last_traded_price, "capital": capital, "shares": number_of_shares}
