from collections import Counter, defaultdict
import datetime
from django.core.management.base import BaseCommand, CommandError
from djfb.models import *
import mlbgame
import pdb


class Command(BaseCommand):
    help = 'Load games for a given day'

  #  def add_arguments(self, parser):
  #      parser.add_argument('year', type=int)
  #      parser.add_argument('month', type=int)
  #      parser.add_arguement'day', type=int)

    def handle(self, *args, **options):

        year = 2018
        month = 9
        day = 1

        games = mlbgame.day(year, month, day)

        for game in games:

            print('Loading game {} at {}'.format(game.away_team,
                                                 game.home_team))

            # create the game model
            try:
                away_team = (MLB_Team
                             .objects
                             .get(common_name=game.away_team,
                                  mlb_division__mlb_league__mlb_season__year=year)
                             )
            except MLB_Team.DoesNotExist:
                away_team = (MLB_Team
                             .objects
                             .get(full_name__icontains=game.away_team,
                                  mlb_division__mlb_league__mlb_season__year=year)
                             )

            try:
                home_team = (MLB_Team
                             .objects
                             .get(common_name=game.home_team,
                                  mlb_division__mlb_league__mlb_season__year=year)
                             )
            except MLB_Team.DoesNotExist:
                home_team = (MLB_Team
                             .objects
                             .get(full_name__icontains=game.home_team,
                                  mlb_division__mlb_league__mlb_season__year=year)
                             )

            try:
                winning_team = (MLB_Team
                                .objects
                                .get(common_name=game.w_team,
                                     mlb_division__mlb_league__mlb_season__year=year)
                                )
            except MLB_Team.DoesNotExist:
                winning_team = (MLB_Team
                                .objects
                                .get(full_name__icontains=game.w_team,
                                     mlb_division__mlb_league__mlb_season__year=year)
                                )

            try:
                losing_team = (MLB_Team
                               .objects
                               .get(common_name=game.l_team,
                                    mlb_division__mlb_league__mlb_season__year=year)
                               )
            except MLB_Team.DoesNotExist:
                losing_team = (MLB_Team
                               .objects
                               .get(full_name__icontains=game.l_team,
                                    mlb_division__mlb_league__mlb_season__year=year)
                               )

            mlb_game = (MLB_Game
                        .objects
                        .get_or_create(gd_id=game.game_id,
                                       date=game.date,
                                       away_team=away_team,
                                       home_team=home_team,
                                       away_team_runs=game.away_team_runs,
                                       home_team_runs=game.home_team_runs,
                                       winning_team=winning_team,
                                       losing_team=losing_team
                                       )[0]
                        )

            # load stats for the players in the game
            stats = mlbgame.player_stats(mlb_game.gd_id)
            events = mlbgame.game_events(mlb_game.gd_id)

            # sort events by player -- needed to get single, double, etc

            batter_events = defaultdict(list)

            for inning in events:
                for pa in inning.top + inning.bottom:
                    batter_events[pa.batter].append(pa.event)

            # batting stats
            for player_stats in stats.away_batting + stats.home_batting:
                try:
                    player = Player.objects.get(gd_id=player_stats.id)
                except Player.DoesNotExist:
                    print(('{} does not exist'
                           .format(player_stats.name_display_first_last)))
                    continue

                print('Loading stats for {}'.format(player.name_full))

                event_ct = Counter(batter_events[player.gd_id])
                pbs = {'pa': (player_stats.ab +
                              player_stats.bb +
                              player_stats.hbp +
                              player_stats.sac +
                              player_stats.sf +
                              player_stats.d),
                       'ab': player_stats.ab,
                       'h': player_stats.h,
                       'bb': player_stats.bb,
                       'hbp': player_stats.hbp,
                       'single': event_ct['Single'],
                       'double': event_ct['Double'],
                       'triple': event_ct['Triple'],
                       'hr': player_stats.hr,
                       'r': player_stats.r,
                       'rbi': player_stats.rbi,
                       'sb': player_stats.sb,
                       'so': player_stats.so,
                       'pitcher': 'P' in player_stats.pos,
                       'catcher': 'C' in player_stats.pos,
                       'first': '1B' in player_stats.pos,
                       'second': '2B' in player_stats.pos,
                       'third': '3B' in player_stats.pos,
                       'short': 'SS' in player_stats.pos,
                       'left': 'LF' in player_stats.pos,
                       'center': 'CF' in player_stats.pos,
                       'right': 'RF' in player_stats.pos,
                       'dh': 'DH' in player_stats.pos,
                       }

                bg = (Batter_Game
                      .objects
                      .update_or_create(
                          player=player,
                          mlb_game=mlb_game,
                          defaults=pbs
                      )[0])

            # pitching stats
            for player_stats in stats.away_pitching + stats.home_pitching:
                try:
                    player = Player.objects.get(gd_id=player_stats.id)
                except Player.DoesNotExist:
                    print(('{} does not exist'
                           .format(player_stats.name_display_first_last)))
                    continue

                print('Loading stats for {}'.format(player.name_full))

                pps = {'w': bool(player_stats.__dict__.get('win')),
                       'l': bool(player_stats.__dict__.get('loss')),
                       'sv': bool(player_stats.__dict__.get('save')),
                       'outs': player_stats.out,
                       'so': player_stats.so,
                       'bb': player_stats.bb,
                       'h': player_stats.h,
                       'hr': player_stats.hr,
                       'er': player_stats.er,
                       'r': player_stats.r,
                       'bf': player_stats.bf,
                       'game_score': player_stats.game_score
                       }

                pg = (Pitcher_Game
                      .objects
                      .update_or_create(
                          player=player,
                          mlb_game=mlb_game,
                          defaults=pps
                      )[0])
