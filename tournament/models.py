from django.db import models
from django.db.models import Sum


class Team(models.Model):
    """Model representing a team"""
    name = models.CharField(unique=True, max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def goals_count(self):
        goals = self.players.aggregate(Sum('goals')).get('goals__sum', )
        return goals or 0


class Player(models.Model):
    """Model representing a player who is always on a team"""
    name = models.CharField(max_length=255, null=False, blank=False)
    goals = models.IntegerField(default=0)
    team = models.ForeignKey(Team, related_name='players', null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.team.name)
