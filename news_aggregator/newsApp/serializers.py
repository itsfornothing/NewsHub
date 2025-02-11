from rest_framework import serializers
from .models import NewsArticle

class NewsArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ['news_id', 'title','description','url','urltoimage','source','category','published_date']


