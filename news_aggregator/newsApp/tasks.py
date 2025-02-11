import os
from celery import shared_task
import requests
from datetime import date
from datetime import timedelta
from .models import FetchLog, NewsArticle, RandomNews
import random
from dotenv import load_dotenv



load_dotenv()

@shared_task
def fetch_all():

    today = date.today()
    yester_day = today - timedelta(days = 1)
    categories_dict = {}
    url = "https://newsapi.org/v2/everything"
    catagories = ['Technology', 'Sports', 'Health', 'Business', 'Politics']

    for element in catagories:
        params = {
        'q': element,
        'from': yester_day,
        'to': today,
        'sortBy': 'popularity',
        'apiKey':  os.getenv("API_KEY")
        }


        response = requests.get(url=url, params=params)
        response.raise_for_status()
        data = response.json()
        categories_dict[element] = data['articles']

        print("it's fetching!")
    if categories_dict:

        for key, value in categories_dict.items():
            i = 5
            for articles in value:
                if i > 0:
                    article = NewsArticle(title=articles['title'], description=articles['description'], url=articles['url'],
                                            urltoimage=articles.get('urlToImage', ''), source=articles['source']['name'],
                                                category=key, published_date=articles['publishedAt'])
                    article.save()
                    i -= 1

    
    

@shared_task
def getrabdom_news_once():
    catagories = ['Technology', 'Sports', 'Health', 'Business', 'Politics']
    if not FetchLog.was_fetched_today():
        print("it's fetching!")
        for item in catagories:
            item_based = NewsArticle.objects.filter(category=item)
            random_news = random.choices(item_based, k=4) if item_based else []
            for article in random_news:
                RandomNews.objects.create(
                    title=article.title,
                    description=article.description,
                    url=article.url,
                    urltoimage=article.urltoimage,
                    source=article.source,
                    category=article.category,
                    published_date=article.published_date
                )

        FetchLog.objects.create()
 

        