from .base_rest_client import BaseRestClient
from models.post import PostModel


class PostRestClient(BaseRestClient):
    model = PostModel
