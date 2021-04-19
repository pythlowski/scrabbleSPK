from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from .models import Room
from .models import DictionaryWord
import time
import os
import random

# Create your views here.

@api_view(['GET'])
def roomList(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def roomDetails(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createRoom(request):
    serializer = RoomSerializer(data=request.data)

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

@api_view(['GET'])
def updateDictionary(request):
    DictionaryWord.objects.all().delete()
    print("XD")
    before = DictionaryWord.objects.all().count()
    start = time.time()
    DictionaryWord.objects.bulk_create([DictionaryWord(word=word) for word in open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'slowa.txt'), 'r').readlines()])
    after = DictionaryWord.objects.all().count()

    return Response({'before': before, 'after': after, 'time': time.time() - start})


@api_view(['GET'])
def getRandomWord(request):
    start = time.time()
    words = DictionaryWord.objects.all()
    word = random.choice(words)
    return Response({'word': word.word, 'time': time.time() - start})