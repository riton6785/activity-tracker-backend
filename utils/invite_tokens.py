from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import os

INVITE_SECRET = os.getenv("INVITE_SECRET", "dev-invite-secret")
INVITE_SALT = "project-invite-salt"
TOKEN_MAX_AGE_SECONDS = 7 * 24 * 3600  # 7 days

serializer = URLSafeTimedSerializer(INVITE_SECRET, salt=INVITE_SALT)

def make_invite_token(invite_id: int, nonce: str) -> str:
    return serializer.dumps({"invite_id": invite_id, "nonce": nonce})

def parse_invite_token(token: str):
    try:
        return serializer.loads(token, max_age=TOKEN_MAX_AGE_SECONDS)  # dict
    except SignatureExpired:
        return "expired"
    except BadSignature:
        return None
