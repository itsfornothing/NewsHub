import random
import string
import smtplib
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from .models import NewsArticle, UserModel, RandomNews, NewBookmark
from .form import UserForm
from rest_framework.views import APIView
from .serializers import NewsArticleSerializers
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from dotenv import load_dotenv
import os
from django.contrib import messages



load_dotenv()


def apikey_generator():
    length = 15
    chars = string.ascii_letters + string.digits
    apikey = ''.join(random.choices(chars, k=length))

    return apikey


def send_email(request):
    my_gmail = os.getenv("MY_GMAIL")
    password = os.getenv("PASSWORD")
    email = request.POST.get('email')

    if not email:
        return HttpResponse("<h1 style='color:red;'>Please enter an email address.</h1>", status=400)

    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  
            connection.login(user=my_gmail, password=password)
            user_instance = UserModel.objects.get(email=email)
            connection.sendmail(from_addr=my_gmail,
                                to_addrs=email,
                                msg=f"Subject:Hello {user_instance.username}\n\nYou Subscribed To NewsHub Newsletter!")
                
            return HttpResponse("<h1 style='color:green;'>Successfully Subscibed, We Sent You an Email!</h1>", status=200)
                
    except UserModel.DoesNotExist:
        return HttpResponse("<h1 style='color:green;'>User With This Email Doesn't Exist!</h1>", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    



def register_view(request):
    message = ''
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            if User.objects.filter(username=username).exists():
                message = 'Username is already taken, please choose another one.'
                return render(request, 'register.html', {'form': form, 'message': message})

            if UserModel.objects.filter(email=email, username=username).exists():
                message = 'You already have an account, please login instead!'
                return render(request, 'register.html', {'form': form, 'message': message})

            else:
                api_key = apikey_generator()
                user = User.objects.create_user(username=username,password=password,email=email)
                newuser = UserModel(username=username,email=email, password=password, api_key=api_key)
                newuser.save()
                login(request,user)
                return redirect('home') 

    else:
        form = UserForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        if email and password:
            user_instance = UserModel.objects.get(email=email)
            user = authenticate(request,username=user_instance.username, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                error_message = 'Invalid Credential!'

        else:
            error_message = 'Please provide both email and password.'
    
    return render(request, 'login.html', {'error_message': error_message})



def logingout(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    

@login_required
def documentacion_view(request):
    current_user = request.user
    user = UserModel.objects.filter(email=current_user.email).first()
    user_apikey = user.api_key
    return render(request, 'documentation.html', {'api_key': user_apikey})


@login_required
def add_bookmark(request, news_id):

    news = get_object_or_404(NewsArticle, news_id=news_id)
    current_user = get_object_or_404(UserModel, email=request.user.email)

    
    bookmark = NewBookmark.objects.filter(user=current_user, news_article=news).first()

    if bookmark:
        bookmark.delete()  
        messages.success(request, "Bookmark deleted successfully!")
    else:
        NewBookmark.objects.create(user=current_user, news_article=news)
        messages.success(request, "Bookmarked successfully!")

    return redirect('view_bookmarks')
    
@login_required
def show_bookmarks(request):
    
    current_user = get_object_or_404(UserModel, email=request.user.email)
    bookmarked = NewBookmark.objects.filter(user=current_user)
    return render(request, 'bookmarks.html', {'News': bookmarked})
    

def home(request):
    count = NewsArticle.objects.count() - 25
    today_news = NewsArticle.objects.filter(news_id__gte=count+1)
    return render(request, 'home.html', {'News': today_news})

def tech_catagorie(request):
    count = NewsArticle.objects.count() - 25
    today_tech_news = NewsArticle.objects.filter(news_id__gte=count+1, category='Technology')
    tech_news = NewsArticle.objects.filter(category='Technology')
    random_news = RandomNews.objects.filter(category='Technology')
    return render(request, 'tech.html', {'today': today_tech_news, 'all': tech_news, 'random': random_news})

def sport_catagorie(request):
    count = NewsArticle.objects.count() - 25
    today_sport_news = NewsArticle.objects.filter(news_id__gte=count+1, category='Sports')
    sport_news = NewsArticle.objects.filter(category='Sports')
    random_news = RandomNews.objects.filter(category='Sports')
    return render(request, 'sport.html', {'today': today_sport_news, 'all': sport_news, 'random': random_news})


def health_catagorie(request):
    count = NewsArticle.objects.count() - 25
    today_health_news = NewsArticle.objects.filter(news_id__gte=count+1, category='Health')
    health_news = NewsArticle.objects.filter(category='Health')
    random_news = RandomNews.objects.filter(category='Health')
    return render(request, 'health.html', {'today': today_health_news, 'all': health_news, 'random': random_news})

def business_catagorie(request):
    count = NewsArticle.objects.count() - 25
    today_business_news = NewsArticle.objects.filter(news_id__gte=count+1, category='Business')
    business_news = NewsArticle.objects.filter(category='Business')
    random_news = RandomNews.objects.filter(category='Business')
    return render(request, 'business.html', {'today': today_business_news, 'all': business_news, 'random': random_news})

def politics_catagorie(request):
    count = NewsArticle.objects.count() - 25
    today_politics_news = NewsArticle.objects.filter(news_id__gte=count+1, category='Politics')
    politics_news = NewsArticle.objects.filter(category='Politics')
    random_news = RandomNews.objects.filter(category='Politics')
    return render(request, 'politics.html', {'today': today_politics_news, 'all': politics_news, 'random': random_news})



class ApiViews(APIView):
    def get_user_by_api_key(self, api_key):
       current_user = self.request.user
       return UserModel.objects.filter(api_key=api_key, email=current_user.email).first()

    def get(self, request, api_key, news_id=None, format=None):
        user = self.get_user_by_api_key(api_key)

        if not user:
            return Response({'error': "Invalid API Key!"}, status=status.HTTP_403_FORBIDDEN)
        
        if news_id:
            news = get_object_or_404(NewsArticle, pk=news_id)
            serializer = NewsArticleSerializers(news)
            return Response(serializer.data)
            
        else:
            all_news = NewsArticle.objects.all()
            serializer =  NewsArticleSerializers(all_news, many=True)
            return Response(serializer.data)
        