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
    name_full = models.CharField(max_length=50)
    name_use = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)
    position_primary = models.IntegerField()
    height_ft = models.IntegerField()
    height_in = models.IntegerField()
    weight = models.IntegerField()
    throws = models.CharField(max_length=2)
    bats = models.CharField(max_length=2)
    debut = models.DateField()
    birth = models.DateField()

    def __str__(self):
        return(self.name_full)
