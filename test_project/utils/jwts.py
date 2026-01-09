import jwt

from typing import Any

def create_access_token(payload:dict[str, Any]) -> str:
    return jwt.encode(payload, key="Hello", algorithm="HS256")

def decode_access_token(token:str) -> dict[str, Any]:
    payload = jwt.decode(token, key="Hello", algorithms=["HS256"])
    return payload