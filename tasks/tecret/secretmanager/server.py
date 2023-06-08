import base64
import hmac
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI(
    title='SecretManager',
    description='A service for serve secrets',
    version='99.9.68',
    redoc_url=None,
)
security = HTTPBasic()


def get_flag(user: str) -> str:
    PREFIX = "ugra_test1ng_in_pr0duc7ion_"
    FLAG_SECRET = b"WJxDMZ6VzHS_6Dpu82TEH76cadrU"
    SUFFIX_SIZE = 12
    flag = PREFIX + hmac.new(
        FLAG_SECRET,
        user.encode(),
        "sha256",
    ).hexdigest()[:SUFFIX_SIZE]
    return flag


class Secret(BaseModel):
    value: str
    expire_at: datetime


def hash_secret(name: str) -> str:
    hs = []
    h = abs(hash(name))
    while h != 0:
        h, v = divmod(h, 256)
        hs.append(v)
    return base64.b64encode(bytes(hs)).decode()


def get_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    return credentials.username

@app.get(
    '/flag',
    tags=['secrets'],
)
def flag(user: str = Depends(get_user)):
    return Secret(value=get_flag(user), expire_at=datetime.now() + timedelta(hours=2))

@app.get(
    '/secret/{name}',
    tags=['secrets'],
    responses={'404': {
        'description': 'Secret not found'
    }},
)
async def get_secret(name: str, user: str = Depends(get_user)) -> Secret:
    value = hash_secret(name)
    return Secret(value=value, expire_at=datetime.now() + timedelta(hours=2))
