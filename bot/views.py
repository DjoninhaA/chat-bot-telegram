import logging
from django.shortcuts import render
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings  # Para carregar o token de settings

# Configurar logging para capturar informações
logger = logging.getLogger(__name__)

# Obtenha o token do bot (Agora usando variáveis de ambiente para segurança)
TOKEN = settings.TELEGRAM_TOKEN

# Inicialize a aplicação globalmente
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou seu bot.')

# Adicione o handler para o comando /start
application.add_handler(CommandHandler("start", start))

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        logger.info("Recebido POST no webhook: %s", request.body.decode('UTF-8'))
        update = Update.de_json(json.loads(request.body.decode('UTF-8')))
        application.process_update(update)
        return JsonResponse({'status': 'ok'})
    logger.warning("Método não suportado: %s", request.method)
    return JsonResponse({'status': 'not ok'})


def set_telegram_webhook():
    """
    Define o webhook no Telegram para receber atualizações
    """
    webhook_url = f'https://thick-feet-beam.loca.lt/webhook/'    # Atualize com o seu domínio
    response = requests.get(
        f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}'
    )
    if response.status_code == 200:
        logger.info("Webhook configurado com sucesso.")
    else:
        logger.error("Erro ao configurar o webhook: %s", response.text)

# Configure o webhook ao iniciar a aplicação
set_telegram_webhook()


def config_bot(request):
    return render(request, 'bot.html')

def home_bot(request):
    return render(request, 'login.html')
