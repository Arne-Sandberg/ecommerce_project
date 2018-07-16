import os
import json
from functools import wraps

import time

from logger.log import setup_logger, INFO, DEBUG


def retry(fn, retries=3, back_off=1.0, exceptions=(TimeoutError, IOError, ConnectionError)):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        final_exception = None
        for _ in range(0, retries):
            try:
                DEBUG("Trying (%s/%s):" % (_ + 1, retries))
                time.sleep(_ * back_off)
                result = fn(*args, *kwargs)
                if result:
                    return result
            except exceptions as e:
                final_exception = e
                pass
        if final_exception:
            DEBUG("Max retries reached for %s with %s" % (fn.__name__, final_exception))

    return wrapper


def log_requests(fn):
    @wraps(fn)
    def logged_fn(*args, **kwargs):
        INFO('Initiating API request')
        response = fn(*args, **kwargs)
        if response.ok:
            INFO('Request successful with status %s' % response.status_code)
        else:
            INFO('Request failed with status %s' % response.status_code)
        data = response.content
        try:
            data = json.dumps(json.loads(response.content), indent=2)
        except Exception as e:
            DEBUG("Failed to load response %s" % e)
        DEBUG("Response Body: %s" % data)
        return response

    return logged_fn
