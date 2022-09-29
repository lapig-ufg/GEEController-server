from functools import wraps
from flask import request
from ServeStatus.config import settings

def is_lapig_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.args.get('key') or not request.args.get('key') == settings.KEYAPI:
            return 'bad request!', 401
        return f(*args, **kwargs)
   
    return wrap