from django.http import HttpResponse
from django.shortcuts import render
from djfb.models import *


def index(request):
    return HttpResponse('Hello World')


def mlb_season_overview(request, season_yr):
    season = MLB_Season.objects.get(year=season_yr)

    context = {
        'season': season
    }

    return render(
        request,
        'djfb/mlb_season_overview.html',
        context
    )


def mlb_team_profile(request, team_id):
    team = MLB_Team.objects.get(id=team_id)

    context = {
        'team': team,
    }

    return render(
        request,
        'djfb/mlb_team_profile.html',
        context
    )
