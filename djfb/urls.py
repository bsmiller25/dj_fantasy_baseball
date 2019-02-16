from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mlb/season/<season_yr>/', views.mlb_season_overview, name='mso'),
]
