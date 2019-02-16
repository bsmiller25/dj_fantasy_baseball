from django.core.management.base import BaseCommand, CommandError
from djfb.models import *
import datetime
import mlbgame
import pdb


class Command(BaseCommand):
    help = 'Load MLB structure information'
    def handle(self, *args, **options):

        year = datetime.datetime.now().year

        mlb_season = MLB_Season.objects.get_or_create(year=year)[0]

        mlb_info = mlbgame.info.team_info()

        for team in mlb_info:
            mlb_league = (MLB_League
                          .objects
                          .get_or_create(mlb_season=mlb_season,
                                         name=team['league'])[0]
                          )

            mlb_division = (MLB_Division
                            .objects
                            .get_or_create(mlb_league=mlb_league,
                                           name=team['division'])[0]
                            )

            print('Loading: ' + team['club_common_name'])
            mlb_team = (MLB_Team
                        .objects
                        .get_or_create(mlb_division=mlb_division,
                                       full_name=team['club_full_name'],
                                       common_name=team['club_common_name'],
                                       url=team['url_prod'],
                                       team_id=team['team_id'],
                                       primary_color=team['primary'],
                                       secondary_color=team['secondary'],
                                       tertiary_color=team['tertiary'],
                                       )[0]
                        )
