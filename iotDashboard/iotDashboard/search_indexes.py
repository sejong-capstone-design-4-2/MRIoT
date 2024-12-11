# myapp/search_indexes.py

from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl.connections import connections
from .models import Article

connections.create_connection(hosts=['localhost'])

class ArticleDocument(Document):
    title = Text()
    content = Text()

    class Index:
        name = 'articles'

    @classmethod
    def prepare_title(cls, instance):
        return instance.title

    @classmethod
    def prepare_content(cls, instance):
        return instance.content
