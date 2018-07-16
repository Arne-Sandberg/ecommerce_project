from .base_model import BaseModel


class PostModel(BaseModel):
    API_SUFFIX = ''
    DOCUMENT_NAME = 'posts'
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, **kwargs):
        super(PostModel, self).__init__(**kwargs)
