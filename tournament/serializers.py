#
# Created by Osmany Castro.
# Copyright © 2021. All rights reserved.
#

from rest_framework import serializers

from tournament import models


class TeamSerializer(serializers.ModelSerializer):
    """Serializer to obtain the Team data"""

    class Meta:
        model = models.Team
        fields = ['id', 'name', 'city', 'created_at', 'updated_at', 'goals_count']


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer to obtain the Player data"""

    class Meta:
        model = models.Player
        fields = ['id', 'name', 'goals', 'team', 'created_at', 'updated_at']


class PlayerTeamSerializer(serializers.ModelSerializer):
    """Serializer to obtain full Player data"""

    team = TeamSerializer()

    class Meta:
        model = models.Player
        fields = ['id', 'name', 'goals', 'team', 'created_at', 'updated_at']
