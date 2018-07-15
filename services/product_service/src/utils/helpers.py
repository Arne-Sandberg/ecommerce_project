import os
import json
from functools import wraps
from logger.log import setup_logger, INFO, DEBUG


def retry(fn, retries=3):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        for _ in range(retries):
            try:
                results = fn(*args, *kwargs)
                if results:
                    break
            except:
                pass

    return wrapper


def log_requests(fn):
    debug = os.environ.get('DEBUG', False)

    @wraps(fn)
    def logged_fn(*args, **kwargs):
        INFO('INITIATING API request')
        if debug:
            pass
        response = fn(*args, **kwargs)
        if response.ok:
            INFO('Request successful with status %s' % response.status_code)
        else:
            INFO('Request failed with status %s' % response.status_code)
        if debug:
            data = response.content
            try:
                data = json.dumps(json.loads(response.content), indent=2)
            except:
                pass
            print(data)
        return response

    return logged_fn
