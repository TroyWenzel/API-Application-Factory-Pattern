from datetime import datetime, timedelta, timezone
from jose import jwt
from functools import wraps
from flask import request, jsonify
import jose.exceptions

SECRET_KEY = "your_secret_key"

def encode_token(user_id, role="user"):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=0, hours=1),
        "iat": datetime.now(tz=timezone.utc),
        "sub": str(user_id), #VERY IMPORTANT, SET YOUR USER ID AS STRING
        "role": role
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def token_required(f): #f stands for the function being decorated/wrapped
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer", "").strip()
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.logged_in_mechanic_id = data['sub']
        except jose.exceptions.JWTError:
            return jsonify({"error": "Token is invalid!"}), 401
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 403
        
        return f( *args, **kwargs)
    return decorated



