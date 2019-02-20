import datetime
from django.db import models


# MLB models
class MLB_Season(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return(str(self.year))


class MLB_League(models.Model):
    name = models.CharField(max_length=50)
    mlb_season = models.ForeignKey('MLB_Season',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return('{} - {}'.format(self.name,
                                self.mlb_season.year)
               )


class MLB_Division(models.Model):
    name = models.CharField(max_length=50)
    mlb_league = models.ForeignKey('MLB_League',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return('{} {} - {}'.format(self.mlb_league
                                   .mlb_season.year,
                                   self.mlb_league.name,
                                   self.name)
               )


class MLB_Team(models.Model):
    full_name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    team_id = models.IntegerField()
    primary_color = models.CharField(max_length=8)
    secondary_color = models.CharField(max_length=8)
    tertiary_color = models.CharField(max_length=8)

    mlb_division = models.ForeignKey('MLB_Division',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return('{} - {}'.format(self.full_name,
                                self.mlb_division
                                .mlb_league
                                .mlb_season.year)
               )

# Player models


class Player(models.Model):
    gd_id = models.IntegerField()
    name_full = models.CharField(max_length=50)
    name_use = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)
    position = models.CharField(max_length=2)
    height_ft = models.IntegerField()
    height_in = models.IntegerField()
    weight = models.IntegerField()
    throws = models.CharField(max_length=2)
    bats = models.CharField(max_length=2)
    debut = models.DateField(null=True, blank=True)
    birth = models.DateField()

    def __str__(self):
        return(self.name_full)


class Roster(models.Model):
    player = models.ForeignKey('Player',
                               on_delete=models.CASCADE)
    team = models.ForeignKey('MLB_Team',
                             on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['player__name_last']

    def __str__(self):
        return('{} - {}'.format(
            self.player.name_full,
            self.team.full_name)
        )


# MLB games and stats
class MLB_Game(models.Model):
    gd_id = models.IntegerField()
    date = models.DateTimeField()
    away_team = models.ForeignKey('MLB_Team',
                                  related_name='away_team_game_set',
                                  on_delete=models.CASCADE)
    home_team = models.ForeignKey('MLB_Team',
                                  related_name='home_team_game_set',
                                  on_delete=models.CASCADE)
    away_team_runs = models.IntegerField()
    home_team_runs = models.IntegerField()

    def __str__(self):
        return('{}: {} at {}'.format(
            datetime.date.strftime(self.date),
            self.away_team__name,
            self.home_team__name
        ))


class Batter_Game(models.Model):
    mlb_game = models.ForeignKey('MLB_Game',
                                 on_delete=models.CASCADE)
    player = models.ForeignKey('Player',
                               on_delete=models.CASCADE)
    h = models.IntegerField()
    bb = models.IntegerField()
    hbp = models.IntegerField()
    single = models.IntegerField()
    double = models.IntegerField()
    triple = models.IntegerField()
    hr = models.IntegerField()
    r = models.IntegerField()
    rbi = models.IntegerField()
    sb = models.IntegerField()
    so = models.IntegerField()
    pitcher = models.BooleanField()
    catcher = models.BooleanField()
    first = models.BooleanField()
    second = models.BooleanField()
    third = models.BooleanField()
    short = models.BooleanField()
    left = models.BooleanField()
    center = models.BooleanField()
    right = models.BooleanField()
    dh = models.BooleanField()

    def __str__(self):
        return('{}: {} at {} -- {}'.format(
            datetime.date.strftime(self.date),
            self.away_team__name,
            self.home_team__name,
            self.player__name_full
        ))


class Pitcher_Game(models.Model):
    mlb_game = models.ForeignKey('MLB_Game',
                                 on_delete=models.CASCADE)
    player = models.ForeignKey('Player',
                               on_delete=models.CASCADE)
    w = models.BooleanField()
    l = models.BooleanField()
    sv = models.BooleanField()
    ip = models.IntegerField()
    so = models.IntegerField()
    bb = models.IntegerField()
    h = models.IntegerField()
    hr = models.IntegerField()
    er = models.IntegerField()
    r = models.IntegerField()
    bf = models.IntegerField()
    bk = models.IntegerField()
    game_score = models.IntegerField()

    def __str__(self):
        return('{}: {} at {} -- {}'.format(
            datetime.date.strftime(self.date),
            self.away_team__name,
            self.home_team__name,
            self.player__name_full
        ))
