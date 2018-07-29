from .base_model import BaseModel


class ProductModel(BaseModel):
    API_SUFFIX = 'v1'
    DOCUMENT_NAME = 'products'

    def __init__(self, **kwargs):
        super(ProductModel, self).__init__(**kwargs)
