import json

from bson import ObjectId
from django.views import View

from api.v1.models.item import Item
from api.v1.models.partner import Partner
from api.v1.utils.api_helpers import APIHelpers
from api.v1.utils.base_model_view import BaseModelView
from api.v1.utils.exceptions import UpdateException


class PartnerItemsView(View):
    @APIHelpers.handle_api_exceptions
    def get(self, request, *args, **kwargs):
        partner_id = kwargs['partner_id']
        partner = BaseModelView.base_find_by_id(Partner, partner_id)
        return BaseModelView.base_get(
            Item, partner_id=partner_id, paginate=False, only="id", **request.GET.copy()
        )

    @APIHelpers.handle_api_exceptions
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        item_id = body["item_id"]
        partner_id = kwargs['partner_id']
        partner = BaseModelView.base_find_by_id(Partner, partner_id)
        item = BaseModelView.base_find_by_id(Item, item_id)
        if item.get('partner_id'):
            existing_partner_id = str(item.get('partner_id'))
            if existing_partner_id != partner_id:
                raise UpdateException(status=APIHelpers.CONFLICT,
                                      message="Partner [%s] already registered to the Item" % partner.get("name",
                                                                                                          partner_id))

        return BaseModelView.base_patch(Item, item_id, {
            "partner_id": partner_id
        })


class PartnerItemView(View):
    @APIHelpers.handle_api_exceptions
    def delete(self, request, *args, **kwargs):
        partner_id = kwargs['partner_id']
        item_id = kwargs['item_id']
        partner = BaseModelView.base_find_by_id(Partner, partner_id)
        item = BaseModelView.base_find_by_id(Item, item_id)
        return BaseModelView.base_patch(Item, item, {
            "partner_id": None
        })
