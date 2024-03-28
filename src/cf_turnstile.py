import requests

from fastapi import HTTPException

from config import settings


URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'


class CloudFlareTurnstile:

    @classmethod
    def check(cls, token: str, remote_ip: str) -> bool:
        if not settings.cf_turnstile_secret_key:
            return True
        try:
            res = requests.post(URL, json={
                "secret": settings.cf_turnstile_secret_key,
                "response": token,
            }, headers={
                "Content-Type": "application/json",
            }).json()
            if res.get("success"):
                return True
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"CloudFlare Turnstile error: {e}"
            )
        raise HTTPException(
            status_code=400, detail="CloudFlare Turnstile error"
        )
