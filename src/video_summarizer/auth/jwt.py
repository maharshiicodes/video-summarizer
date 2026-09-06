import os
import jwt
from datetime import timedelta , datetime , timezone
from dotenv import load_dotenv
from jwt.exceptions import PyJWTError
load_dotenv()
SECRET = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
expiry = 60 * 72

def create_acces_token(user_id : str) -> str:
    payload = {
        "sub" : user_id,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes = expiry)
    }

    token = jwt.encode(payload,SECRET,algorithm = ALGORITHM
    return token

def decode_access_token(token : str) -> str | None:
    try:
        payload = jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None