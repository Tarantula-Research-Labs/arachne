# token_manager.py

import boto3

PARAM_NAME = "/trading/access_token"

def get_access_token():
    ssm = boto3.client("ssm", region_name="ap-south-1")

    response = ssm.get_parameter(
        Name=PARAM_NAME,
        WithDecryption=True
    )

    return response["Parameter"]["Value"]