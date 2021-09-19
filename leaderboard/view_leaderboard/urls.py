from django.urls import path
from . import views

app_name = 'view_leaderboard'

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
]