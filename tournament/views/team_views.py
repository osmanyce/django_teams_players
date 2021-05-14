from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from tournament.models import Team
from tournament.serializers import TeamSerializer
from tournament.utils.enums import ResponseStatus
from tournament.utils.response_data import json_data

NO_TEAMS = 'No teams found'


class TeamListView(ListAPIView):
    """API to list Teams"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Customize the query by params"""
        try:
            params = self.request.GET
            name = params.get('name', )
            city = params.get('city', )
            queryset_list = self.queryset.order_by('name')
            if name:
                queryset_list = queryset_list.filter(name__contains=name.lower())
            if city:
                queryset_list = queryset_list.filter(city__contains=city.lower())
            return queryset_list
        except ValueError:
            return None

    def get(self, request, **kwargs):
        try:
            data = TeamSerializer(self.get_queryset(), many=True).data
            return Response(json_data(data=data), status=status.HTTP_200_OK)
        except Exception as error:
            return Response(json_data(
                data=str(error), status=ResponseStatus.FAILED, message='Failed To Get content.'
            ), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeamManageAPIView(APIView):
    """API to get, create, update or delete a Team"""

    @staticmethod
    def get(request):
        # find team
        team = TeamManageAPIView.get_team(request.GET['id'])
        if not team:
            return Response(json_data(status=ResponseStatus.FAILED, message=NO_TEAMS), status=status.HTTP_404_NOT_FOUND)
        # serialize and return team
        data = TeamSerializer(team).data
        return Response(json_data(data=data), status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        # serialize sent data
        serialized_request = TeamSerializer(data=request.data)
        # validate and save data
        if serialized_request.is_valid():
            serialized_request.save()
            return Response(json_data(data=serialized_request.data), status=status.HTTP_200_OK)
        return Response(json_data(
            status=ResponseStatus.FAILED, message=serialized_request.errors), status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def put(request):
        # find team
        team = TeamManageAPIView.get_team(request.GET['id'])
        if not team:
            return Response(json_data(status=ResponseStatus.FAILED, message=NO_TEAMS), status=status.HTTP_404_NOT_FOUND)
        # serialize team
        serialized_data = TeamSerializer(instance=team, data=request.data)
        # validate and save data
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(json_data(data=serialized_data.data), status=status.HTTP_200_OK)
        return Response(json_data(
            status=ResponseStatus.FAILED, message=serialized_data.errors), status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def delete(request):
        # find team
        team = TeamManageAPIView.get_team(request.GET['id'])
        if not team:
            return Response(json_data(status=ResponseStatus.FAILED, message=NO_TEAMS), status=status.HTTP_404_NOT_FOUND)
        # delete founded team
        team.delete()
        return Response(json_data(message='Deleted'), status=status.HTTP_200_OK)

    @staticmethod
    def get_team(pk):
        try:
            return Team.objects.get(id=pk)
        except ObjectDoesNotExist:
            return None
