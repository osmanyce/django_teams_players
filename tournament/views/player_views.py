from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from tournament.models import Player
from tournament.serializers import PlayerSerializer, PlayerTeamSerializer
from tournament.utils.enums import ResponseStatus
from tournament.utils.response_data import json_data

NO_PLAYERS = 'No players found'


class PlayerListView(ListAPIView):
    """API to list Players"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Customize the query by params"""
        try:
            params = self.request.GET
            name = params.get('name', )
            team_name = params.get('team', )
            queryset_list = self.queryset.order_by('name')
            if name:
                queryset_list = queryset_list.filter(name__contains=name.lower())
            if team_name:
                queryset_list = queryset_list.filter(team__name__contains=team_name.lower())
            return queryset_list
        except ValueError:
            return None

    def get(self, request, **kwargs):
        try:
            data = PlayerSerializer(self.get_queryset(), many=True).data
            return Response(json_data(data=data), status=status.HTTP_200_OK)
        except Exception as error:
            return Response(json_data(
                data=str(error), status=ResponseStatus.FAILED, message='Failed To Get content.'
            ), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlayerManageAPIView(APIView):
    """APIs to get, create, update or delete a Player"""

    @staticmethod
    def get(request):
        # find player
        player = PlayerManageAPIView.get_player(request.GET['id'])
        if not player:
            return Response(json_data(
                status=ResponseStatus.FAILED, message=NO_PLAYERS), status=status.HTTP_404_NOT_FOUND
            )
        # serialize and return player
        data = PlayerTeamSerializer(player).data
        return Response(json_data(data=data), status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        data = request.data
        # serialize sent data
        serialized_request = PlayerSerializer(data=data)
        # validate and save data
        if serialized_request.is_valid():
            serialized_request.save()
            return Response(json_data(data=serialized_request.data), status=status.HTTP_200_OK)
        return Response(json_data(
            status=ResponseStatus.FAILED, message=serialized_request.errors), status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def put(request):
        data = request.data
        # find player
        player = PlayerManageAPIView.get_player(request.GET['id'])
        if not player:
            return Response(json_data(
                status=ResponseStatus.FAILED, message=NO_PLAYERS), status=status.HTTP_404_NOT_FOUND
            )
        # serialize player
        serialized_data = PlayerSerializer(instance=player, data=data)
        # validate and save data
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(json_data(data=serialized_data.data), status=status.HTTP_200_OK)
        return Response(json_data(
            status=ResponseStatus.FAILED, message=serialized_data.errors), status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def delete(request):
        # find player
        player = PlayerManageAPIView.get_player(request.GET['id'])
        if not player:
            return Response(json_data(
                status=ResponseStatus.FAILED, message=NO_PLAYERS), status=status.HTTP_404_NOT_FOUND
            )
        # delete founded player
        player.delete()
        return Response(json_data(message='Deleted'), status=status.HTTP_200_OK)

    @staticmethod
    def get_player(pk):
        try:
            return Player.objects.get(id=pk)
        except ObjectDoesNotExist:
            return None
