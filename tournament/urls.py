#
# Created by Osmany Castro.
# Copyright © 2021. All rights reserved.
#
from django.urls import path

from tournament.views import team_views, player_views

urlpatterns = [
    path('teams/', team_views.TeamListView.as_view()),
    path('manage/team/', team_views.TeamManageAPIView.as_view()),
    path('players/', player_views.PlayerListView.as_view()),
    path('manage/player/', player_views.PlayerManageAPIView.as_view())
]
