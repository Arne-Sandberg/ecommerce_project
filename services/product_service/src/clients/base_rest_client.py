import json
import requests
from models.product import ProductModel
from utils.constants import BASE_URL
from utils.custom_expections import APIException, OperationNotSupported
from utils.helpers import retry, log_requests
from logger.log import (setup_logger, INFO, DEBUG, TRACE)


class BaseRestClient(object):
    model = None
    def __init__(self, *args, **kwargs):
        self.model = self.__class__.model
        setup_logger()

    @log_requests
    def __get(self, url, params):
        response = requests.get(url=url, params=params)
        return response

    @log_requests
    def __post(self, url, data):
        pass

    @log_requests
    def __put(self, url, data):
        pass

    @log_requests
    def __patch(self, url, data):
        pass

    @log_requests
    def __delete(self, url):
        pass

    def __make_request(self, method, url, *args, **kwargs):
        __METHODS = {
            'GET': self.__get,
            'POST': self.__post,
            'PUT': self.__put,
            'DELETE': self.__delete,
        }

        if method not in __METHODS:
            raise OperationNotSupported

        func = __METHODS[method]
        url = url.lstrip('/')
        if not url.startswith('http'):
            base_url = self.model.BASE_URL
            if not base_url:
                base_url = BASE_URL
            base_url = base_url.lstrip('/')

            url = '%s/%s' % (base_url, url)

        response = func(url, *args, **kwargs)

        if response.ok:
            result = json.loads(response.content)
            return result
        else:
            raise APIException(
                '[%s] API request failed for %s' % (method, url))

    @retry
    def get_one(self, id):
        url = "%s/%s/%s" % (self.model.API_SUFFIX,
                            self.model.DOCUMENT_NAME, id)
        data = self.__make_request('GET', url)
        if data:
            model = self.model(data)
            return model
        else:
            raise APIException('%s not found' % id)


    @retry
    def get(self, params=None):
        url = "%s/%s" % (self.model.API_SUFFIX,
                         self.model.DOCUMENT_NAME)
        data = self.__make_request('GET', url)
        if data:
            models = list()
            for d in data:
                model = self.model(d)
                models.append(model)
            return models
        else:
            raise APIException('%s not found' % id)


    def create(self, data):
        pass

    def save(self, data):
        pass
