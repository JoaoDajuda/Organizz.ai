import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")

def enviar_email(destinatario: str, assunto: str, corpo_html: str):
    mensagem = MIMEMultipart("alternative")
    mensagem["Subject"] = EMAIL_REMETENTE
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = destinatario
    mensagem.attach(MIMEText(corpo_html, "html"))

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.sendmail(EMAIL_REMETENTE, destinatario, mensagem.as_string())