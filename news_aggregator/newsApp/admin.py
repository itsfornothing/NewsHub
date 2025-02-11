from django.contrib import admin
from .models import NewsArticle, RandomNews

# Register your models here.
admin.site.register(NewsArticle)
admin.site.register(RandomNews)
