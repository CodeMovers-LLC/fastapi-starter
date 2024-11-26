import requests
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os

COGNITO_POOL_ID = os.getenv("COGNITO_POOL_ID")
COGNITO_REGION = os.getenv("COGNITO_REGION")
COGNITO_JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json"

def get_jwks():
    response = requests.get(COGNITO_JWKS_URL)
    response.raise_for_status()
    return response.json()

def verify_cognito_token(token: str) -> dict:
    jwks = get_jwks()
    try:
        # Decode the token's header to get the key ID
        headers = jwt.get_unverified_header(token)
        kid = headers["kid"]
        # Find the correct key from the JWKS
        key = next(k for k in jwks["keys"] if k["kid"] == kid)
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

        # Decode and verify the token
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=os.getenv("COGNITO_CLIENT_ID"),  # Verify the token's audience
            issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}"
        )
        return payload
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except InvalidTokenError as e:
        raise Exception(f"Invalid token: {e}")
