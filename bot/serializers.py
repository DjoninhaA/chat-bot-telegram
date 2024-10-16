from rest_framework import serializers

from .models import Bot

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id', 'Bot_name', 'Bot_Description')