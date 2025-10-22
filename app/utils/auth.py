# app/utils/auth.py
from fastapi import Header, HTTPException, status

API_KEY = "supersecret123"  # you can change this
API_KEY_NAME = "x-api-key"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
