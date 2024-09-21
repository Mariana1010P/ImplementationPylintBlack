"""
api_key_auth.py

This module provides functionality to handle API key authentication using FastAPI.
"""

import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

# Load environment variables from a .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "x-api-key"

# Create an API key header instance for security
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Retrieve and validate the API key from the request header.

    Args:
        api_key (str): The API key provided in the request header.

    Returns:
        str: The valid API key if it matches the expected value.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "status": False,
            "status_code": status.HTTP_403_FORBIDDEN,
            "message": "Unauthorized",
        },
    )
