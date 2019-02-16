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
