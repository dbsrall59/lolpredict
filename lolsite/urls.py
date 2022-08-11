"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('search/', views.search),
    path('join/', views.join),
    path('dbjoin/', views.dbjoin),
    path('login/', views.login),
    path('dblogin/', views.dblogin),
    path('logout/', views.logout),
    path('board/', views.board),
    path('writeboard/', views.writeBoard),
    path('writeComplete/', views.writeComplete),
    path('boardcontent/<int:boardid>/', views.boardcontent),
    path('writereply/<int:boardid>/', views.writereply),
]
