import jwt
import time
import uuid
from fastapi import FastAPI, HTTPException
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Replace these values with your own Apple developer account information
team_id = '5NMJ2A479W'
client_id = 'com.footballtarkow.com'
key_id = '73YATAJ963'
private_key_path = 'AuthKey_73YATAJ963.p8'
app = FastAPI()


def revoke_token(token, client_secret):
    revoke_url = "https://appleid.apple.com/auth/revoke"

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "token": token,
        "token_type_hint": "refresh_token"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(revoke_url, data=data, headers=headers)

    if response.status_code == 200:
        print("Token revoked successfully.")
    else:
        print("Token revocation failed with status code:", response.status_code)

    return response
    
def generate_client_secret():
    # Load the private key from the file
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Create the JWT payload with the required claims
    claims = {
        'iss': team_id,
        'iat': int(time.time()),
        'exp': int(time.time()) + 15777000,  # Expiration time (180 days)
        'aud': 'https://appleid.apple.com',
        'sub': client_id,
        'jti': str(uuid.uuid4()),  # Unique identifier for the token
    }

    # Sign the JWT using the private key
    client_secret = jwt.encode(claims, private_key, algorithm='ES256', headers={'kid': key_id})

    return client_secret

apple_token_revocation_url = 'https://appleid.apple.com/auth/token'

@app.post('/revoke-token')
def revoke(token: str):
    if not token:
        raise HTTPException(status_code=400, detail='Token is missing.')

    try:
        client_secret = generate_client_secret()
        response = revoke_token(token, client_secret)
        print(f"STATUS CODE: {response.status_code}")
        if response.status_code == 200:
            return {'success': True}
        else:
            raise HTTPException(status_code=400, detail='Token revocation failed.')
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail='Internal server error.')
    

# token = "eyJraWQiOiJZdXlYb1kiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLmZvb3RiYWxsdGFya293LmNvbSIsImV4cCI6MTY5MTMxNzgxMCwiaWF0IjoxNjkxMjMxNDEwLCJzdWIiOiIwMDE3NTguNmQ4ODZlMzQwNDkyNDA1ZThmODU0ZDkxZDRjZGMwNTguMTUyNyIsImNfaGFzaCI6IjVPc1gwaEJnNVIxQmxwMEJxSXoxRXciLCJlbWFpbCI6IjhmMnBza2t2dGhAcHJpdmF0ZXJlbGF5LmFwcGxlaWQuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiaXNfcHJpdmF0ZV9lbWFpbCI6InRydWUiLCJhdXRoX3RpbWUiOjE2OTEyMzE0MTAsIm5vbmNlX3N1cHBvcnRlZCI6dHJ1ZX0.wG1izbJ44AT8n0sJirwkRMhk5mIemxzhGad2YWzehwud7OrvOiG5_Qayd5NqGiHRDkRm1faFeX94f2xLlpAe34vz_ejtexdYQAychfb6a9-xw1tSysZh33W31cRwIcuf6zYXuoQS9b_Xs37w1rhzrA2RgfyZcGGPjV83JwpOnSODauvSR4RbLPYMVpIV4zqNw1qcd2I2Lh3_lXSvYmijm4g1GRJNGYOFxv7d2LAixNhZrbC3B6sHOFdLXCbOba-0GWqSZnGEHcXBV-u8ymcTgebWzhhCy5HKrccr4fYKbyncOiycRdAtT7651toeapD1oSqOk2R6UfdjdCpYaHMiXg"
# client_secret = generate_client_secret()
# response = revoke_token(token, client_secret)