import os
import jwt

from fastapi import Request
from requests.structures import CaseInsensitiveDict

# For testing requests

ADMIN_HEADER = CaseInsensitiveDict(
    data={"Cookie":
          'Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1hbmFnZXIiLCJuYW1lIjoiRnVsYW5vIGRlIFRhbCIsImpvYl9yb2xlIjoiRXN0YWdpYXJpbyIsImFjY2VzcyI6ImFkbWluIn0.vu3T9_4xAf2UWL8n4c-Wm3pM8JZTAmwdBubrFWgX7nM'})  # noqa 501
MANAGER_HEADER = CaseInsensitiveDict(
    data={"Cookie":
    'Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1hbmFnZXIiLCJuYW1lIjoiRnVsYW5vIGRlIFRhbCIsImpvYl9yb2xlIjoiRXN0YWdpYXJpbyIsImFjY2VzcyI6Im1hbmFnZXIifQ.zftUNuBvt8G19eq0Wqvnd52wBuxzIatQLcSpwIrWkUQ'})  # noqa 501
BASIC_HEADER = CaseInsensitiveDict(
    data={"Cookie":
    'Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1hbmFnZXIiLCJuYW1lIjoiRnVsYW5vIGRlIFRhbCIsImpvYl9yb2xlIjoiRXN0YWdpYXJpbyIsImFjY2VzcyI6ImJhc2ljIn0.YOEKPNoyA5xK0X4R1z3KNB-v9E2Oy1AokmzArx-2bks'})  # noqa 501


ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def decode_access_token(encoded_jwt: str) -> str:
    return jwt.decode(encoded_jwt, key=JWT_SECRET_KEY,
                      algorithms=[ALGORITHM])['access']


def get_authorization(request: Request) -> str:
    authorization = request.cookies.get('Authorization')
    if authorization:
        auth = decode_access_token(authorization)
    else:
        auth = 'public'
    return auth
