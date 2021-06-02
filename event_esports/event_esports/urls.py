from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.getData, name='home'),
    path('dota2/', views.getDotaData, name='dota2'),
    path('lol/', views.getLoLData, name='lol'),
    path('siege/', views.getSiegeData, name='siege'),
    path('csgo/', views.getCsgoData, name='csgo'),
    path('valorant/', views.getValorantData, name='valorant')
]
