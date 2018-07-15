from .base_rest_client import BaseRestClient
from models.product import ProductModel


class ProductRestClient(BaseRestClient):
    model = ProductModel
