from django.db import models
from django.contrib.postgres.fields.array import ArrayField

class Team(models.Model):
    id = models.IntegerField
    acronym = models.CharField
    current_videogame_id = models.IntegerField
    current_videogame_name = models.CharField
    current_videogame_slug = models.CharField
    image_url = models.CharField
    location = models.CharField
    modified_at = models.DateTimeField
    name = models.CharField
    slug = models.CharField

class Match(models.Model):
    name = models.CharField
    rescheduled = models.BooleanField
    league_id = models.IntegerField
    league_image_url = models.CharField
    league_modified_at = models.DateTimeField
    league_image_url = models.CharField
    league_name = models.CharField
    league_url = models.CharField
    league_slug = models.CharField
    opponent1_acronym = models.CharField
    opponent1_id = models.IntegerField
    opponent1_image_url = models.CharField
    opponent1_location = models.CharField
    opponent1_modified_at = models.DateTimeField
    opponent1_name = models.CharField
    opponent1_slug = models.CharField
    opponent2_acronym = models.CharField
    opponent2_id = models.IntegerField
    opponent2_image_url = models.CharField
    opponent2_location = models.CharField
    opponent2_modified_at = models.DateTimeField
    opponent2_name = models.CharField
    opponent2_slug = models.CharField
    forfeit = models.BooleanField
    live_embed_url = models.CharField
    winner = models.CharField
    official_stream_url = models.CharField
    videogame = models.CharField
    begins_at = models.CharField
    begins_in = models.DateTimeField
    formatted_begins_in = models.CharField
    score_team_1 = models.IntegerField
    score_team_2 = models.IntegerField

class Tournament(models.Model):
    begin_at: models.DateTimeField
    end_at: models.DateTimeField
    image_url: models.CharField
    league_name: models.CharField
    league_url: models.CharField
    serie_name: models.CharField
    name: models.CharField
    slug: models.CharField
    tier: models.CharField
    id: models.IntegerField
    begins_in: models.DateTimeField
    standings: ArrayField
