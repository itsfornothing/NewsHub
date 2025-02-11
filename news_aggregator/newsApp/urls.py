from django.urls import path
from . import views
from . views import ApiViews
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.home, name="home"),
    path("technews", views.tech_catagorie, name="technews"),
    path("healthnews", views.health_catagorie, name="healthnews"),
    path("sportsnews", views.sport_catagorie, name="sportsnews"),
    path("politicsnews", views.politics_catagorie, name="politicsnews"),
    path("businessnews", views.business_catagorie, name="businessnews"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logingout, name="logout"),
    path("documentation", views.documentacion_view, name="documentation"),
    path("bookmarks/<int:news_id>", views.add_bookmark, name="bookmarks"),
    path("view_bookmarks", views.show_bookmarks, name="view_bookmarks"),
    path("sendemail", views.send_email, name="sendemail"),
    path('apiviews/<str:api_key>', ApiViews.as_view(), name='apiviews-list'),
    path('apiviews/<int:news_id>/<str:api_key>', ApiViews.as_view(), name='apiviews-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns) # allow your API endpoints to accept format suffixes like .json, .api, or .xml at the end of the URL