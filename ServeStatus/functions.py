from functools import wraps
from flask import request
def is_lapig_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.args.get('key'):
            return 'bad request!', 401
        if not request.args.get('key') == 'LAPIG2022GEE':
            return 'bad request!', 401
        return f(*args, **kwargs)
   
    return wrap