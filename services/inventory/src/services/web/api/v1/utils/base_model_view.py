import json

from django.views import View
from django.http import JsonResponse

from api.v1.utils.exceptions import FailedToCreateException, UpdateException, DeleteException
from api.v1.utils.filters import BaseFilter
from api.v1.utils.helpers import to_json
from api.v1.utils.api_helpers import APIHelpers
from api.v1.utils.constants import (
    MAX_RESULTS_PER_RESPONSE,
)


class BaseModelView(View):
    def __init__(self, model, *args, **kwargs):
        super(BaseModelView, self).__init__(*args, **kwargs)
        self.model = model
        self.model_filter = kwargs.pop('model_filter', BaseFilter)()

    @property
    def model(self):
        return getattr(self, '_model')

    @model.setter
    def model(self, value):
        if not value:
            raise ValueError("Model cannot be None")
        else:
            setattr(self, '_model', value)

    @staticmethod
    @APIHelpers.check_if_entity_exists
    def base_find_by_id(model, model_id):
        result = model.find({
            "id": model_id
        })
        data = to_json(result)[0]
        return data

    @staticmethod
    def base_get(model, model_filter=None, *args, **kwargs):
        skip = int(kwargs.pop('skip', 0))
        limit = int(kwargs.pop('limit', 25))
        paginate = kwargs.pop('paginate', True)
        only = kwargs.pop('only', None)
        sort = kwargs.pop('sort', None)
        search = kwargs.pop('search', None)
        if search:
            query = model_filter.get_filters(search)
        else:
            query = dict(**kwargs)

        if paginate == 'false' or paginate is False:
            limit = MAX_RESULTS_PER_RESPONSE

        results = model.find(
            query, skip=skip, limit=limit,
            projection=only, sort=sort)

        data = to_json(results)
        return JsonResponse({
            "success": True,
            "data": data,
            "total": results.count()
        }, status=APIHelpers.OK)

    @staticmethod
    def base_post(model, data):
        instance_id = model.create(data)
        if instance_id:
            return JsonResponse({
                "success": True,
                "data": BaseModelView.base_find_by_id(model, instance_id)
            }, status=APIHelpers.CREATED)
        raise FailedToCreateException()

    @staticmethod
    @APIHelpers.check_if_entity_exists
    def base_put(model, model_id, data):
        result = model.update(model_id, data)
        if result['Modified']:
            return JsonResponse({
                "success": True,
                "data": [BaseModelView.base_find_by_id(model, model_id)],
                "total": 1
            }, status=APIHelpers.OK)
        return UpdateException()

    @staticmethod
    @APIHelpers.check_if_entity_exists
    def base_patch(model, model_id, data):
        result = model.patch(model_id, data)
        if result['ok']:
            return JsonResponse({
                "success": True,
                "data": [BaseModelView.base_find_by_id(model, model_id)],
                "total": 1
            }, status=APIHelpers.OK)
        return UpdateException()

    @staticmethod
    @APIHelpers.check_if_entity_exists
    def base_delete(model, model_id):
        result = model.delete(model_id)
        if result['ok']:
            return JsonResponse({
                "success": True,
            }, status=APIHelpers.SUCCESSFULLY_DELETED)
        raise DeleteException()

    @APIHelpers.handle_api_exceptions
    def get(self, request):
        return BaseModelView.base_get(self.model, self.model_filter, **request.GET.dict().copy())

    @APIHelpers.handle_api_exceptions
    def post(self, request):
        body = json.loads(request.body)
        return BaseModelView.base_post(self.model, body)


class BaseModelDetailView(View):
    @property
    def model(self):
        return getattr(self, '_model')

    @model.setter
    def model(self, value):
        if not value:
            raise ValueError("Model cannot be None")
        else:
            setattr(self, '_model', value)

    def __init__(self, model, *args, **kwargs):
        super(BaseModelDetailView, self).__init__(*args, **kwargs)
        self.model = model
        self.model_filter = kwargs.pop('model_filter', BaseFilter)()

    @APIHelpers.handle_api_exceptions
    def get(self, request, **kwargs):
        model_id = kwargs['id']
        return BaseModelView.base_get(self.model, id=model_id)

    @APIHelpers.handle_api_exceptions
    def put(self, request, **kwargs):
        model_id = kwargs['id']
        body = json.loads(request.body)
        return BaseModelView.base_put(self.model, model_id, body)

    @APIHelpers.handle_api_exceptions
    def patch(self, request, **kwargs):
        model_id = kwargs['id']
        body = json.loads(request.body)
        return BaseModelView.base_patch(self.model, model_id, body)

    @APIHelpers.handle_api_exceptions
    def delete(self, request, **kwargs):
        model_id = kwargs['id']
        return BaseModelView.base_delete(self.model, model_id)
