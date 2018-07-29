from bson import ObjectId
from django.http import JsonResponse
from django.views import View

from api.v1.models.item import Item
from api.v1.models.product import Product
from api.v1.utils.base_model_view import BaseModelView
from api.v1.utils.api_helpers import APIHelpers


class ProductItemsView(View):
    @APIHelpers.handle_api_exceptions
    def post(self, request, *args, **kwargs):
        product_id = kwargs['id']
        item_id = kwargs['item_id']
        product = BaseModelView.base_find_by_id(Product, product_id)
        item = BaseModelView.base_find_by_id(Item, item_id)
        product_items = product.get('items', [])
        product_items = set(map(str, product_items))
        Product.patch(product_id, {
            "items": map(ObjectId, product_items)
        })
        return BaseModelView.base_get(Product, product_id)
