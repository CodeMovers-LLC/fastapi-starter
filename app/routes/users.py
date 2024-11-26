from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.auth_utils import verify_cognito_token

from fastapi import APIRouter, HTTPException
from typing import List
from app.db import database
from app.models.user_model import User

router = APIRouter()
bearer_scheme = HTTPBearer()

def authenticate_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = verify_cognito_token(token)
        return payload  # Return payload if valid
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/", response_model=List[User])
async def get_users():
    """Fetch all users."""
    query = "SELECT * FROM ce_users"
    try:
        rows = await database.fetch_all(query=query)
        return [User(**row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile")
async def user_profile(user=Depends(authenticate_user)):
    """
    Example protected route.
    """
    return {"message": "User profile", "user": user}