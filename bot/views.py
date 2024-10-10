from django.shortcuts import render

# Create your views here.
def config_bot(request):
    return render(request, 'bot.html')