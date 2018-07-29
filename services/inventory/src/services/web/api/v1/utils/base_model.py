from datetime import datetime
from bson import ObjectId
from web.settings import DB
from api.v1.utils.helpers import (
    merge_patch,
    to_bson,
    get_filters,
    get_projections,
    get_sort_directions,
)


class BaseModel(object):
    __meta__ = dict()

    @classmethod
    def get_collection(cls):
        if 'collection' in cls.__meta__:
            return cls.__meta__['collection']
        return cls.__name__.lower()

    @classmethod
    def find(cls, filter_query, **kwargs):
        extra_filters = to_bson(kwargs)

        query = {
            "filter": get_filters(filter_query),
            "projection": get_projections(extra_filters.pop('projection', None)),
            "sort": get_sort_directions(extra_filters.pop('sort', None)),
            **extra_filters
        }
        return DB[cls.get_collection()].find(**query)

    @classmethod
    def create(cls, data):
        data = to_bson(data)
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        return DB[cls.get_collection()].save(data)

    @classmethod
    def update(cls, model_id, data):
        old = DB[cls.get_collection()].find_one({'_id': ObjectId(model_id)})
        data = to_bson(data)
        data['created_at'] = old.get('created_at', datetime.utcnow())
        data['updated_at'] = datetime.utcnow()
        return DB[cls.get_collection()].update({
            '_id': ObjectId(model_id)}, data
        )

    @classmethod
    def patch(cls, model_id, patch_data):
        patch_data = to_bson(patch_data)
        old = DB[cls.get_collection()].find_one({'_id': ObjectId(model_id)})
        patched_data = merge_patch(old, patch_data)
        return cls.update(model_id, patched_data)

    @classmethod
    def delete(cls, model_id):
        return DB[cls.get_collection()].remove({'_id': ObjectId(model_id)})
