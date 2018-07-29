import json
from json import JSONDecodeError

from bson import ObjectId


class BaseFilter:
    def __init__(self):
        self.filter_keys = {'name'}

    @staticmethod
    def __get_filters_from_string(filter_term):
        _filter = dict()
        try:
            json_dict = json.loads(filter_term)
            if len(json_dict) > 1:
                raise ValueError("Search can only be performed on a single term")
            key = list(json_dict.keys())[0]
            value = json_dict[key]
            if key == 'id':
                key = ['_id']
                value = map(ObjectId, value)
            _filter[key] = {
                "$regex": value,
                "$options": "i"
            }
        except (JSONDecodeError, TypeError):
            _filter = filter_term
        return _filter

    def get_filters(self, filter_term):
        filters = self.__get_filters_from_string(filter_term)

        return self._get_filters(filters)

    def _get_filters(self, filter_to_apply):
        query = {}
        if isinstance(filter_to_apply, dict):
            for key in filter_to_apply:
                query[key] = filter_to_apply[key]
        else:
            query = {
                "$or": []
            }
            for key in self.filter_keys:
                query["$or"].append({
                    key: {
                        "$regex": filter_to_apply,
                        "$options": "i"
                    }
                })
        return query
