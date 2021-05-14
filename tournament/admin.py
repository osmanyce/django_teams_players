from django.contrib import admin

from tournament import models as tournament_models

admin.site.register(tournament_models.Team)
admin.site.register(tournament_models.Player)
