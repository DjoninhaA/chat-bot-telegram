import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Obtenha o token do bot

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        update = Update.de_json(json.loads(request.body.decode('UTF-8')))
        dp.process_update(update)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'not ok'})

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Eu sou seu bot.')

# Configuração do Updater e Dispatcher
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
