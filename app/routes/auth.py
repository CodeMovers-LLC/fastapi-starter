from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.auth_utils import verify_cognito_token

router = APIRouter()
bearer_scheme = HTTPBearer()

@router.post("/login")
def login():
    """
    Example login route.
    In real-world scenarios, this would involve redirecting users to Cognito for authentication.
    """
    return {"message": "Redirect to Cognito login page or initiate OAuth flow"}

@router.get("/validate-token")
def validate_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """
    Validate the AWS Cognito JWT.
    """
    token = credentials.credentials
    try:
        payload = verify_cognito_token(token)
        return {"message": "Token is valid", "payload": payload}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
