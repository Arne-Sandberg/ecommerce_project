from django.urls import re_path

from api.v1.utils.constants import OBJECT_ID_PATTERN
from api.v1.views.partner_item_view import PartnerItemsView, PartnerItemView
from api.v1.views.scheduled_to_dispatch_item_view import ScheduledToDispatchItemView
from api.v1.views.product_item_view import ProductItemsView

urlpatterns = [
    re_path(r'^product/(?P<product_id>%s)/items/?$' % OBJECT_ID_PATTERN, ProductItemsView.as_view()),
    re_path(r'^item/(?P<item_id>%s)/dispatch/?$' % OBJECT_ID_PATTERN, ScheduledToDispatchItemView.as_view()),
    re_path(r'^partner/(?P<partner_id>%s)/items/?$' % OBJECT_ID_PATTERN, PartnerItemsView.as_view()),
    re_path(r'^partner/(?P<partner_id>%s)/items/(?P<item_id>%s?)/?$' % (OBJECT_ID_PATTERN, OBJECT_ID_PATTERN),
            PartnerItemView.as_view())
]
