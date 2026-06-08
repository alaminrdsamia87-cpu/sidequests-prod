import json
import os

import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings


def get_firebase_app():
    if not firebase_admin._apps.get(settings.FIREBASE_APP_NAME):
        cred = _get_credential()
        firebase_admin.initialize_app(cred, name=settings.FIREBASE_APP_NAME)
    return firebase_admin.get_app(settings.FIREBASE_APP_NAME)


def _get_credential():
    path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
    if path and os.path.exists(path):
        return credentials.Certificate(path)
    json_str = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    if json_str:
        return credentials.Certificate(json.loads(json_str))
    raise RuntimeError(
        'Firebase service account not found. Set FIREBASE_SERVICE_ACCOUNT_PATH '
        'or FIREBASE_SERVICE_ACCOUNT env var.'
    )


def verify_firebase_token(id_token):
    app = get_firebase_app()
    try:
        decoded = auth.verify_id_token(id_token, app=app)
        return decoded
    except Exception:
        return None
