import os
from copy import deepcopy

class BaseModel(object):
    API_SUFFIX = None
    DOCUMENT_NAME = None
    BASE_URL = None


    @property
    def base_url(self):
        if self.BASE_URL:
            return self.BASE_URL
        if os.environ.get('DEFAULT_WEBSERVICE_URL', None):
            return os.environ.get('DEFAULT_WEBSERVICE_URL')
        return None

    def __init__(self, **kwargs):
        self.__cache = deepcopy(kwargs)
        self.data = deepcopy(kwargs)

    @property
    def id(self):
        return getattr(self, 'data.id')
