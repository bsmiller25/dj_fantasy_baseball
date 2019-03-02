from django.db.models import Sum, Avg, Q, F, Case, Count, When
from django.db.models.functions import TruncYear
from django.http import HttpResponse
from django.shortcuts import render
from djfb.models import *
import pdb


def index(request):
    context = {
    }
    return render(
        request,
        'djfb/index.html',
        context
    )


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
            .annotate(year=TruncYear('mlb_game__date__year'))
            .values('year')
            .annotate(
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
            )
            .order_by('year')
            )

    # get hitting stats
    bstats = (Batter_Game
              .objects
              .filter(player=player)
              .annotate(year=TruncYear('mlb_game__date__year'))
              .values('year')
              .annotate(pa=Sum('pa'),
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
              .order_by('year')
              )

    for bstats_yr in bstats:
        # batting average
        try:
            bstats_yr['avg'] = round(1.0 * bstats_yr['h'] / bstats_yr['ab'], 3)
        except (ZeroDivisionError, TypeError):
            bstats_yr['avg'] = 0.000

            # on base percentage
            try:
                bstats_yr['obp'] = round((1.0 * bstats_yr['h'] +
                                          bstats_yr['bb']) / bstats_yr['pa'], 3)
            except (ZeroDivisionError, TypeError):
                bstats_yr['obp'] = 0.000

            # slugging percentage
            try:
                bstats_yr['slg'] = round((1.0 * bstats_yr['singles']
                                          + 2.0 * bstats_yr['doubles']
                                          + 3.0 * bstats_yr['triples']
                                          + 4.0 * bstats_yr['hr']) / bstats_yr['ab'], 3)
            except (ZeroDivisionError, TypeError):
                bstats_yr['slg'] = 0.000

    # get pitching stats
    pstats = (Pitcher_Game
              .objects
              .filter(player=player)
              .annotate(year=TruncYear('mlb_game__date__year'))
              .values('year')
              .annotate(
                  w=Count(Case(When(w=True, then=1))),
                  l=Count(Case(When(l=True, then=1))),
                  sv=Count(Case(When(sv=True, then=1))),
                  so=Sum('so'),
                  h=Sum('h'),
                  bb=Sum('bb'),
                  er=Sum('er'),
                  outs=Sum('outs'))
              )

    for pstats_yr in pstats:
        # ERA
        try:
            pstats_yr['era'] = round(
                9.0 * pstats_yr['er'] / pstats_yr['outs']/3, 3)
        except (ZeroDivisionError, TypeError):
            pstats_yr['era'] = 0.000

        # WHIP
        try:
            pstats_yr['whip'] = round(
                1.0 * (pstats_yr['bb'] + pstats_yr['h']) / pstats_yr['outs']/3, 3)
        except (ZeroDivisionError, TypeError):
            pstats_yr['whip'] = 0.000

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
