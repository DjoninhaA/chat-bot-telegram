from django.shortcuts import render
from rest_framework.response import Response



from  .serializers import UserSerializer



def config_bot(request):
    return render(request, 'bot.html')
    
    
def create_bot(request):
    if request.method == 'POST':
        new_bot = request.data

        serializer = UserSerializer(data=new_bot)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    