from fastapi import Request, HTTPException, status
from app.utils.generate_token import verify_access_token, verify_refresh_token


def verify_jwt(request: Request):
    token = request.cookies.get("access-token")
    
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access token not found")
    
    try:
        payload = verify_access_token(token)
        id = payload.get("_id")
        
        if not id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
       
        return {"payload": payload, "userid" : id }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")