import qrcode
from io import BytesIO
from PIL import Image

def gerar_pix_qr_code(valor, chave_pix, descricao):
    """
    Gera um QR Code para pagamento via Pix e retorna a imagem e a string do Pix.
    
    :param valor: Valor do pagamento
    :param chave_pix: Chave Pix do recebedor
    :param descricao: Descrição do pagamento
    :return: Imagem do QR Code e string do Pix
    """
    pix_data = f"00020126360014BR.GOV.BCB.PIX0114{chave_pix}5204000053039865404{valor:.2f}5802BR5913Nome Recebedor6009Cidade12362070503***6304"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pix_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # Salvar a imagem em um buffer de bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer, pix_data

def enviar_pix_qr_code(chat_id, valor, chave_pix, descricao, bot):
    """
    Envia um QR Code de pagamento via Pix para o usuário no Telegram.
    
    :param chat_id: ID do chat do Telegram
    :param valor: Valor do pagamento
    :param chave_pix: Chave Pix do recebedor
    :param descricao: Descrição do pagamento
    :param bot: Instância do bot do Telegram
    """
    qr_code_image, pix_data = gerar_pix_qr_code(valor, chave_pix, descricao)
    bot.send_photo(chat_id, qr_code_image, caption=f"Pagamento via Pix\nValor: R$ {valor:.2f}\nDescrição: {descricao}\n\nString do Pix: {pix_data}")