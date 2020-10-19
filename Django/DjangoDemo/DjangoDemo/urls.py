"""DjangoDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', blog_views.IndexView.as_view(), name="index"), # 設定首頁(http://127.0.0.1:8000/)串接 blog 的 index 這個 view
    path('page1/', blog_views.page1), # 設定首頁(http://127.0.0.1:8000/page1/)串接 blog 的 page1 這個 view
    path('login/', blog_views.LoginView.as_view(), name="login"),
    path('logout/', blog_views.logout, name="logout"),
    path('register/', blog_views.register, name="register"),
    path('article/add/',  blog_views.ArticleCreateView.as_view(), name="article-add"),
    
    path('articles/', blog_views.ArticleList.as_view(), name="article-list"),
    path('articles/<int:pk>/', blog_views.ArticleDetail.as_view(), name='article-detail'),
    path('articles/<int:pk>/update/', blog_views.ArticleUpdateView.as_view(), name='article-update'),
    path('articles/<int:pk>/delete/', blog_views.ArticleDeleteView.as_view(), name='article-delete'),
]
