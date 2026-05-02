import pandas as pd
import webbrowser
from fyers_apiv3 import fyersModel
import boto3

ssm = boto3.client("ssm", region_name="ap-south-1")
PARAM_NAME = "/trading/access_token"


class TokenCreation:

    def __init__(self):

        self.client_id = "W7LM9VJA41-200"
        self.secret_key = "qpKCdzLr6qijQPIR"
        self.redirect_uri = "https://tarantularesearch.com/"
        self.token_response = None,
        self.access_token =  None

    def generate_auth_token(
        self,
    ) -> dict:
        """
        Handles FYERS OAuth flow and returns access token response.

        Returns
        -------
        dict
            Full response containing access_token, refresh_token, expiry, etc.
        """

        # -------------------------------
        # Step 1: Generate auth URL
        # -------------------------------
        session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type="code",
            state="sample_state",
        )

        auth_url = session.generate_authcode()
        # webbrowser.open(auth_url)
        return auth_url

    def generate_access_token(self, raw_url):

        # -------------------------------
        # Step 2: User pastes redirected URL
        # -------------------------------
        # raw_code = input("Paste redirected URL here: ").strip()

        try:
            auth_code = raw_url.split("auth_code=")[1].split("&")[0]
        except IndexError:
            raise ValueError("Invalid redirect URL. Auth code not found.")

        # -------------------------------
        # Step 3: Exchange auth_code for access_token
        # -------------------------------
        session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type="code",
            grant_type="authorization_code",
        )

        session.set_token(auth_code)
        token_response = session.generate_token()
        access_token = token_response["access_token"]
        self.access_token = access_token
        ssm.put_parameter(
            Name=PARAM_NAME,
            Value=access_token,
            Type="SecureString",
            Overwrite=True,
        )
        return {"message": "Token created and saved in params."}

        