from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from djfb.models import *
import datetime
import pdb

import mlbgame


class Command(BaseCommand):
    help = 'Load MLB structure information'

    def add_arguments(self, parser):

        parser.add_argument('year', type=int,
                            nargs='?', default=datetime.date.today().year)

    def handle(self, *args, **options):

        year = options['year']

        # load MLB structure
        call_command('load_MLB_structure', year)

        # TODO load past players

        # for now: load current rosters to at least have current players
        call_command('load_players', year)

        # load games from season
        firstgame = mlbgame.important_dates(year).first_date_seas[:10]
        lastgame = mlbgame.important_dates(year).last_date_seas[:10]
        asg = mlbgame.important_dates(year).all_star_date[:10]

        d = datetime.datetime.strptime(firstgame, '%Y-%m-%d')

        while d < datetime.datetime.strptime(lastgame, '%Y-%m-%d'):
            d += datetime.timedelta(1)
            if d != datetime.datetime.strptime(asg, '%Y-%m-%d'):
                call_command('load_day', d.year, d.month, d.day)

        print('Complete')
