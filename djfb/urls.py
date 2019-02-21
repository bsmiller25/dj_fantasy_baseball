from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mlb/season/<season_yr>/', views.mlb_season_overview, name='mso'),
    path('mlb/team/<team_id>/', views.mlb_team_profile, name='mtp'),
    path('player/<player_id>/', views.player_profile, name='pp'),
]
