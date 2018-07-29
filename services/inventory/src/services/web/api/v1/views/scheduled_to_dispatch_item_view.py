from django.views import View

from api.v1.models.item import Item
from api.v1.utils.api_helpers import APIHelpers
from api.v1.utils.base_model_view import BaseModelView, BaseModelDetailView
from api.v1.utils.constants import TO_BE_DISPATCHED


class ScheduledToDispatchItemView(View):
    @APIHelpers.handle_api_exceptions
    def post(self, request, *args, **kwargs):
        item_id = kwargs['item_id']
        data = {"status": TO_BE_DISPATCHED}
        return BaseModelView.base_patch(Item, item_id, data)
