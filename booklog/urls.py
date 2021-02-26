"""booklog URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from page import views as pageViews
from accounts import views as accountsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pageViews.home, name='home'),
    path('mylibrary', pageViews.mylibrary, name= 'mylibrary'),
    path('add_book/', pageViews.add_book, name='add_book'),
    path('signup/',accountsViews.signup, name='signup'),
    path('login/', accountsViews.login, name='login'),
    path('logout/', accountsViews.logout, name='logout'),
    path('book_api/', pageViews.book_api, name='book_api'),
    path('new_book/', pageViews.new_book, name='new_book'),
    path('detail/<str:isbn>', pageViews.detail, name='detail'),
    path('add_idea/<str:isbn>', pageViews.add_idea, name='add_idea'),
    path('add_score/<str:isbn>', pageViews.add_score, name='add_score'),
    path('idea_detail/<str:isbn>', pageViews.idea_detail, name='idea_detail'),
    path('add_sentence/<str:isbn>', pageViews.add_sentence, name='add_sentence'),
    path('mod_sentence/<int:pk>', pageViews.mod_sentence, name='mod_sentence'),
    path('del_sentence/<int:pk>', pageViews.del_sentence, name='del_sentence'),
    path('index/', pageViews.index, name='index'),
    path('generic/', pageViews.generic, name='generic'),
    path('elements/', pageViews.elements, name='elements'),
    path('search/', pageViews.search, name='search'),
    path('tour/', pageViews.tour, name='tour'),
    path('tour/book/<str:isbn>', pageViews.tour_book, name='tour_book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
