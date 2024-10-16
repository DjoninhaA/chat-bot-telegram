from django.db import models

class Bot(models.Model):

    bot_name = models.CharField(primary_key=True, max_length=100, default='')
    bot_description = models.CharField(max_length=180, default='')


    def __str__(self):
        return f'BotName: {self.bot_name} | Description: {self.bot_description}'