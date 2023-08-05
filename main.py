import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import time
import uvicorn
from fastapi.middleware.cors import CORSMiddleware



# GLOBALS

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_token_expiration = 0

# send request to apple for token revoke

# MODEL

revokeURL = "https://appleid.apple.com/auth/revoke"
teamID = "5NMJ2A479W"
filename = "AuthKey_73YATAJ963.p8"
keyID = "73YATAJ963"
tokenType = "access_token"

class RevokeTokenModel(BaseModel):
    clientID: str
    token: str
    tokenTypeGint: str


def generate_tokenv2(bundleID):
    with open(filename, "r") as f:
        private_key = f.read()
        team_id = teamID
        client_id = bundleID
        key_id = keyID
        validity_minutes = 20
        timestamp_now = int(time.time())
        timestamp_exp = timestamp_now + (60 * validity_minutes)
        # Assuming `last_token_expiration` is a class variable defined somewhere else
        # cls.last_token_expiration = timestamp_exp
        data = {
            "iss": team_id,
            "iat": timestamp_now,
            "exp": timestamp_exp,
            "aud": "https://appleid.apple.com",
            "sub": client_id
        }
        token = jwt.encode(
            payload=data,
            key=private_key.encode('utf-8'),
            algorithm="ES256",
            headers={"kid": key_id}
        )
        return token


def generate_token(bundleID):
    with open(filename, "r") as f:
        private_key = f.read()
    team_id = teamID
    client_id = bundleID
    key_id = keyID
    validity_minutes = 20
    timestamp_now = int(time.time())
    timestamp_exp = timestamp_now + (60 * validity_minutes)

    data = {
        "iss": team_id,
        "iat": timestamp_now,
        "exp": timestamp_exp,
        "aud": "https://appleid.apple.com",
        "sub": client_id
    }
    token = jwt.encode(payload=data, key=private_key, algorithm="ES256", headers={"kid": key_id})
    return token
    
def revoke_token_request(client_secret: str, clientID: str, tokenTypeGint: str, token: str):
    data = {
        "client_id": clientID,
        "client_secret": client_secret,
        "token": token,
        "token_type_hint": tokenTypeGint
    }
    response = requests.post(revokeURL, data=data)
    print(response)
    if response.status_code == 200:
        return True
    else:
        # You can raise an HTTPException here if you want to handle the error differently
        print(f"\n\nRESPONSE -> {response.text}\n\n")
        with open("logs.txt", "w+") as f:
            f.write(response.text)
        print("ERROR")
        raise HTTPException(status_code=response.status_code, detail=response.text)

    


@app.post("/revoke")
def revokeToken(token: str, clientID: str):
    client_secret = generate_token(bundleID=bundleID)
    with open("log1.txt", "w+") as f:
        f.write(client_secret)
    revoked = revoke_token_request(token=token, clientID=clientID, tokenTypeGint=tokenType, client_secret=client_secret)

    return {"token_revoked": revoked}

apple_token_revocation_url = 'https://appleid.apple.com/auth/token'

@app.post('/revoke-token')
async def revoke_token(token: str):
    if not token:
        raise HTTPException(status_code=400, detail='Token is missing.')

    try:
        response = requests.post(
            apple_token_revocation_url,
            data={
                'token': token,
                'client_id': 'your_client_id',
                'client_secret': 'your_client_secret',
            }
        )
        print(f"STATUS CODE: {response.status_code}")
        if response.status_code == 200:
            return {'success': True}
        else:
            raise HTTPException(status_code=400, detail='Token revocation failed.')
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail='Internal server error.')


# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

# token = "eyJraWQiOiJZdXlYb1kiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLmZvb3RiYWxsdGFya293LmNvbSIsImV4cCI6MTY5MTI2MTI0OCwiaWF0IjoxNjkxMTc0ODQ4LCJzdWIiOiIwMDE3NTguNmQ4ODZlMzQwNDkyNDA1ZThmODU0ZDkxZDRjZGMwNTguMTUyNyIsImNfaGFzaCI6InI2NjNWbTYxbTR0VkJfckxyRkZhSnciLCJlbWFpbCI6IjhmMnBza2t2dGhAcHJpdmF0ZXJlbGF5LmFwcGxlaWQuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiaXNfcHJpdmF0ZV9lbWFpbCI6InRydWUiLCJhdXRoX3RpbWUiOjE2OTExNzQ4NDgsIm5vbmNlX3N1cHBvcnRlZCI6dHJ1ZX0.TkZtkIgljXOhCc1bp4YAx77yfZOBYz6iHDE3fxIi_l4oSjwOjM1xxUr9rkKEnOriJgHBChTop-CmGlM3zvh4taXwP_ZTb-xzQL9UeQtElM53f9l4w2j-PWfGrjxiX8Dyuyor-vbcxlKtUIcsVFIcDikHWQsI1iLYU40mn7x-399MdSFqyKqIarfk1P6TuBK3Fwf9EBYvPWrizXfFV1v5Kc-7p1mEbV3OChrMXEgLAvmhUWcFg95GKzhglbnHg2NOSWijeDfDFTuZC8EEPDplEhV86RzLi47jrksGReGQteVl8-LobLusceFrvRB-xAIWstEDl6al9SJ4dIAanGnBVA"
# bundleID = "com.footballtarkow.com"
# keyID = "73YATAJ963"


# client_secret = generate_tokenv2(bundleID)
# revoke_token_request(client_secret,bundleID,tokenType, token)