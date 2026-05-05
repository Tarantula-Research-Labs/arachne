from fyers_apiv3 import fyersModel
from authentication import get_access_token

# def exit_position(connect):
#     fyers = fyersModel.FyersModel(
#         client_id=connect.get("client_id"),
#         token=get_access_token(),
#         is_async=False,
#         log_path="",
#     )
#     data = {
#         "segment":[10],
#         "side":[1,-1],
#         "productType":["INTRADAY"]
#        }

#     response = fyers.exit_positions(data=data)
#     return response

def create_exit_position(orderType,ltp):
    if orderType == 1:
        orderType = "short"
        limitPrice = ltp
    else:
        orderType="long"
        limitPrice = ltp

    return orderType, limitPrice


def exit_position(connect, ticker, numberOfShares, order_type, ltp):

    orderType, limitPrice = create_exit_position( order_type,ltp)

    fyers = fyersModel.FyersModel(
        client_id=connect.get("client_id"),
        token=get_access_token(),
        is_async=False,
        log_path="",
    )
    print(order_type)
    data = {
        "symbol": ticker,
        "qty": numberOfShares,
        "type": 1,
        "side": 1 if orderType == "long" else -1,
        "productType": "INTRADAY",
        "limitPrice":limitPrice,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "donchianBreakout",
        "isSliceOrder": False,
    }
    response = fyers.place_order(data=data)
    return response
