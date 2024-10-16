from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from rest_framework.decorators import api_view


from  .serializers import UserSerializer



def config_bot(request):
    return render(request, 'bot.html')

def home_bot(request):
    return render(request, 'home_bot.html')
    
@api_view(['POST'])   
def create_bot(request):
    if request.method == 'POST':
        new_bot = request.data

        serializer = UserSerializer(data=new_bot)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    