from django.db import models
from django.utils.timezone import now


# Create your models here.

class NewsArticle(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=1000)
    urltoimage = models.URLField(max_length=1000, null=True, blank=True)
    source = models.CharField(max_length=500)
    category = models.CharField(max_length=100, default='')
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"News with ID: {self.news_id} - Title: {self.title} - Category: {self.category}"
    


class UserModel(models.Model):
    username = models.CharField(max_length=20, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    api_key = models.CharField(max_length=15)


class FetchLog(models.Model):
    last_fetched = models.DateField(auto_now=True)

    @classmethod
    def was_fetched_today(cls):
        """Check if data was fetched today."""
        return cls.objects.filter(last_fetched=now().date()).exists()


class RandomNews(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=1000)
    urltoimage = models.URLField(max_length=1000, null=True, blank=True)
    source = models.CharField(max_length=500)
    category = models.CharField(max_length=100, default='')
    published_date = models.DateField(auto_now_add=True)



class NewBookmark(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)  
    news_article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)  

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} bookmarked {self.news_article.title}"