from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from .models import Room
import time
import os
import random

# Create your views here.

@api_view(['GET'])
def roomList(request):
    rooms = Room.objects.all()
    rooms = list(filter(lambda x: x.is_public, rooms))
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def roomDetails(request, pk):
    room = Room.objects.get(code=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createRoom(request):
    if not request.session.exists(request.session.session_key):
        return Response('Cannot create a room for a user without a session.')

    serializer_data = request.data
    serializer_data['host_name'] = request.session['nickname']
    serializer = RoomSerializer(data=serializer_data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(instance=room, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    room.delete()

    return Response('Room deleted.')


@api_view(['POST'])
def nicknameSession(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
        request.session['nickname'] = request.data['nickname']
        return Response('Session created.')
    else:
        request.session['nickname'] = request.data['nickname']
        return Response('Session nickname updated.') 

    
