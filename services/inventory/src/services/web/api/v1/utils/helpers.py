import re
import pymongo
import pytz
from bson import ObjectId
from datetime import datetime
from dateutil import parser

from pymongo.cursor import Cursor

from api.v1.utils.constants import OBJECT_ID_PATTERN, ISO_DATETIME_REGEX


def is_object_id(str_id):
    regex = re.compile(OBJECT_ID_PATTERN, re.IGNORECASE)
    return regex.match(str_id)


def is_iso_datetime(str_datetime):
    regex = re.compile(ISO_DATETIME_REGEX, re.IGNORECASE)
    return regex.match(str_datetime)


def to_bson(data):
    if type(data) in (list, tuple):
        values = []
        for datum in data:
            values.append(to_bson(datum))
        return values
    elif isinstance(data, dict):
        item = dict()
        for key, value in data.items():
            item[key] = to_bson(value)
        return item
    elif isinstance(data, str):
        if is_iso_datetime(data):
            return parser.parse(data, tzinfos=pytz.utc)
        elif is_object_id(data):
            return ObjectId(data)
    return data


def to_json(data):
    if isinstance(data, Cursor) or type(data) in (list, tuple):
        values = []
        for datum in data:
            values.append(to_json(datum))
        return values
    elif isinstance(data, dict):
        item = dict()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                if key == '_id':
                    key = 'id'
                item[key] = str(value)
            elif isinstance(value, datetime):
                item[key] = value.astimezone().isoformat()
            elif isinstance(value, dict):
                item[key] = to_json(value)
            else:
                item[key] = value
        return item
    else:
        return data


def get_filters(query_dict):
    filters = dict()
    if 'id' in query_dict:
        query_dict['_id'] = query_dict.pop('id')
    for key, value in query_dict.items():
        values = value
        if isinstance(value, str):
            values = {
                '$in': values.split(',')
            }
        filters[key] = values

    return to_bson(filters)


def get_projections(projection_list):
    projections = dict()
    if isinstance(projection_list, str):
        projection_list = projection_list.split(',')
    if type(projection_list) in (list, tuple):
        for projection in projection_list:
            projections[projection] = 1
    return projections if len(projections) > 0 else None


def get_sort_directions(sort_by):
    sort_directions = list()
    if isinstance(sort_by, str):
        sort_by = sort_by.split(',')
    if type(sort_by) in (list, tuple):
        for sort_name in sort_by:
            sort_dir = pymongo.ASCENDING
            if sort_name[0] in ('+', '-'):
                sort_dir = pymongo.ASCENDING if sort_name[0] == '+' else pymongo.DESCENDING  # -1
                sort_name = sort_name[1:]
            sort_directions.append((sort_name, sort_dir))
    return sort_directions if len(sort_directions) > 0 else None


def merge_patch(target, patch):
    """
    This is supposed to be a JSON merge patch implementation.
    @link https://tools.ietf.org/html/rfc7386
    :param target: The original dict that is supposed to be patched
    :type target: dict
    :param patch: The patch dict
    :type patch: dict
    :return: Modified target dict
    :rtype: dict, any
    """
    if isinstance(patch, dict):
        if not isinstance(target, dict):
            target = {}  # Ignore the contents and set it to an empty Object
        for key, value in patch.items():
            if value is None:
                if key in target:
                    del target[key]
            else:
                target[key] = merge_patch(target.get(key), value)
        return target
    else:
        return patch
