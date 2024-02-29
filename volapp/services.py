import jwt
from django.conf import settings
from datetime import datetime, timedelta
from pytz import timezone
from .models import *

def verify_tokens(access_token: str, refresh_token: str):
    try:
        decrypted_access = jwt.decode(access_token, settings.SECRET_KEY, "HS256")
        current_datetime = datetime.now(timezone(settings.TIME_ZONE))
        decrypted_access['expiry'] = datetime.strptime(decrypted_access['expiry'], "%Y-%m-%d %H:%M:%S%z")
        if decrypted_access['expiry'] < current_datetime:
            decrypted_refresh = jwt.decode(refresh_token, settings.SECRET_KEY, "HS256")
            decrypted_refresh['expiry'] = datetime.strptime(decrypted_refresh['expiry'], "%Y-%m-%d %H:%M:%S%z")
            if decrypted_refresh['expiry'] < current_datetime or decrypted_refresh['access'] != access_token:
                return None
            else:
                new_access_token = jwt.encode({'email': decrypted_access['email'], 'expiry': (current_datetime + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S%z")},
                                              settings.SECRET_KEY,
                                              "HS256")
                new_refresh_token = jwt.encode({'access': new_access_token, 'expiry': (current_datetime + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S%z")})
                return {'email': decrypted_access['email'], 'access': new_access_token, 'refresh': new_refresh_token}
        else:
            return {'email': decrypted_access['email'], 'access': access_token, 'refresh': refresh_token}
    except Exception as e:
        return None
    
def create_token(email: str):
    current_datetime = datetime.now(timezone(settings.TIME_ZONE))
    access_token = jwt.encode({'email': email, 'expiry': (current_datetime + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S%z")}, settings.SECRET_KEY, "HS256")
    refresh_token = jwt.encode({'access': access_token, 'expiry': (current_datetime + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S%z")}, settings.SECRET_KEY, "HS256")
    return access_token, refresh_token