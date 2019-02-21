from django.db.models import Sum, Avg, Q, F, Case, Count, When
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

    # eligibility

    elig = (Batter_Game
            .objects
            .filter(player=player)
            .aggregate(
                p=Count(Case(When(pitcher=True, then=1))),
                ut=Count(Case(When(pitcher=False, then=1))),
                c=Count(Case(When(catcher=True, then=1))),
                fb=Count(Case(When(first=True, then=1))),
                sb=Count(Case(When(second=True, then=1))),
                tb=Count(Case(When(third=True, then=1))),
                ss=Count(Case(When(short=True, then=1))),
                lf=Count(Case(When(left=True, then=1))),
                cf=Count(Case(When(center=True, then=1))),
                rf=Count(Case(When(right=True, then=1))),
                dh=Count(Case(When(dh=True, then=1)))
            ))

    # get hitting stats
    bstats = (Batter_Game
              .objects
              .filter(player=player)
              .aggregate(pa=Sum('pa'),
                         ab=Sum('ab'),
                         h=Sum('h'),
                         r=Sum('r'),
                         hr=Sum('hr'),
                         rbi=Sum('rbi'),
                         sb=Sum('sb'),
                         bb=Sum('bb'),
                         singles=Sum('single'),
                         doubles=Sum('double'),
                         triples=Sum('triple'),
                         )
              )

    # batting average
    try:
        bstats['avg'] = round(1.0 * bstats['h'] / bstats['ab'], 3)
    except (ZeroDivisionError, TypeError):
        bstats['avg'] = 0.000

    # on base percentage
    try:
        bstats['obp'] = round((1.0 * bstats['h'] +
                               bstats['bb']) / bstats['pa'], 3)
    except (ZeroDivisionError, TypeError):
        bstats['obp'] = 0.000

    # slugging percentage
    try:
        bstats['slg'] = round((1.0 * bstats['singles']
                               + 2.0 * bstats['doubles']
                               + 3.0 * bstats['triples']
                               + 4.0 * bstats['hr']) / bstats['ab'], 3)
    except (ZeroDivisionError, TypeError):
        bstats['slg'] = 0.000

    # get pitching stats
    pstats = (Pitcher_Game
              .objects
              .filter(player=player)
              .aggregate(w=Count(Case(When(w=True, then=1))),
                         l=Count(Case(When(l=True, then=1))),
                         sv=Count(Case(When(sv=True, then=1))),
                         so=Sum('so'),
                         h=Sum('h'),
                         bb=Sum('bb'),
                         er=Sum('er'),
                         outs=Sum('outs'))
              )

    # ERA
    try:
        pstats['era'] = round(9.0 * pstats['er'] / pstats['outs']/3, 3)
    except (ZeroDivisionError, TypeError):
        pstats['era'] = 0.000

    # WHIP
    try:
        pstats['whip'] = round(
            1.0 * (pstats['bb'] + pstats['h']) / pstats['outs']/3, 3)
    except (ZeroDivisionError, TypeError):
        pstats['whip'] = 0.000

    context = {
        'player': player,
        'elig': elig,
        'bstats': bstats,
        'pstats': pstats,
    }

    return render(
        request,
        'djfb/player_profile.html',
        context
    )
