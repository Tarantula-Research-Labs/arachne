from fyers_apiv3 import fyersModel

def place_single_order(connect, ticker, numberOfShares, order_type):
    fyers = fyersModel.FyersModel(
        client_id=connect.get("client_id"),
        token=connect.get("access_token"),
        is_async=False,
        log_path="",
    )
    print(order_type)
    data = {
        "symbol": f"NSE:{ticker}-EQ",
        "qty": numberOfShares,
        "type": 2,
        "side": 1 if order_type == "long" else -1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "donchianBreakout",
        "isSliceOrder": False,
    }
    response = fyers.place_order(data=data)
    return response
