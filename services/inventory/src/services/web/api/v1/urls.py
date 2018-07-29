import inspect
from importlib import import_module

from django.urls import re_path, include, path

from api.v1.utils.base_model import BaseModel
from api.v1.utils.base_model_view import BaseModelView, BaseModelDetailView
from api.v1.utils.constants import OBJECT_ID_PATTERN
from api.v1.views import urls as view_urls

def get_base_model_views(model_dir):
    base_model_views = []
    models = import_module(model_dir)
    for model_name in models.__all__:
        module = import_module(model_dir + '.' + model_name)
        for attr in dir(module):
            module_attr = getattr(module, attr)
            if inspect.isclass(module_attr) and module_attr != BaseModel \
                    and issubclass(module_attr, BaseModel):
                api_endpoint = '^%s/?$' % module_attr.get_collection()
                detail_api_endpoint = '^%s/(?P<id>%s)/?$' % (
                    module_attr.get_collection(),
                    OBJECT_ID_PATTERN
                )
                base_model_views.extend([
                    re_path(api_endpoint, BaseModelView.as_view(
                        model=module_attr)),
                    re_path(detail_api_endpoint,
                            BaseModelDetailView.as_view(model=module_attr))
                ])
    return base_model_views


urlpatterns = []
urlpatterns.extend(get_base_model_views('api.v1.models'))
urlpatterns.extend(view_urls.urlpatterns)
