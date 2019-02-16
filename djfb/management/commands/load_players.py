from django.core.management.base import BaseCommand, CommandError
from djfb.models import *
import datetime
import mlbgame
import pdb


class Command(BaseCommand):
    help = 'Load Players'
    def handle(self, *args, **options):

        teams = MLB_Team.objects.all()

        for team in teams:

            old_roster = Roster.objects.filter(team=team,
                                               end__isnull=True)

            new_roster = mlbgame.info.roster(team.team_id)

            current_roster = []

            for player in new_roster['players']:

                try:
                    pro_debut = (datetime
                                 .datetime
                                 .strptime(
                                     player['pro_debut_date'],
                                     '%Y-%m-%dT00:00:00')
                                 )
                except ValueError:
                    # player has not made debut yet
                    pro_debut = None

                pvar = {
                    'name_full': player['name_full'],
                    'name_use': player['name_use'],
                    'name_last': player['name_last'],
                    'position': player['position_txt'],
                    'height_ft': player['height_feet'],
                    'height_in': player['height_inches'],
                    'weight': player['weight'],
                    'throws': player['throws'],
                    'bats': player['bats'],
                    'debut': pro_debut,
                    'birth': (datetime
                              .datetime
                              .strptime(
                                  player['birth_date'],
                                  '%Y-%m-%dT00:00:00')
                              )
                }

                print('Loading: ' + player['name_full'])
                p = (Player
                     .objects
                     .get_or_create(gd_id=player['player_id'],
                                    defaults=pvar)[0]
                     )

                r = (Roster
                     .objects
                     .get_or_create(team=team,
                                    player=p,
                                    start=(datetime
                                           .datetime
                                           .strptime(
                                               player['start_date'],
                                               '%Y-%m-%dT00:00:00')
                                           )
                                    )[0]
                     )

                current_roster.append(r)

            # add end date to players no longer on roster
            for rost_pos in old_roster:
                if rost_pos not in current_roster:
                    rost_pos.end = datetime.datetime.today().date()
                    ros_pos.save()
