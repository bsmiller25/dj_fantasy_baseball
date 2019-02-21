from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from djfb.models import *
import pdb


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


def player_profile(request, player_id):
    player = Player.objects.get(id=player_id)

    stats = (Batter_Game
             .objects
             .filter(player=player)
             .aggregate(Sum('ab'),
                        Sum('h'),
                        Sum('r'),
                        Sum('hr'),
                        Sum('rbi'),
                        Sum('sb'))
             )

    try:
        avg = round(1.0 * stats['h__sum'] / stats['ab__sum'], 3)
    except ZeroDivisionError:
        avg = 0.000

    context = {
        'player': player,
        'avg': avg,
        'r': stats['r__sum'],
        'hr': stats['hr__sum'],
        'rbi': stats['rbi__sum'],
        'sb': stats['sb__sum'],
    }

    return render(
        request,
        'djfb/player_profile.html',
        context
    )
