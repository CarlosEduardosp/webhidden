from flask_sqlalchemy import SQLAlchemy
from app import db, user
import  random
import smtplib
import email.message


def validar_entrada(nome, email, banco):
    for pessoa in banco:
        if nome == pessoa[0].nome:
            return True
        elif email == pessoa[0].email:
            return False


def enviar_email(dados):
    nome = f'{dados[3]}'.upper()

    corpo_email = f"<p>Olá {dados[0]}, Veja Quem é Seu Amigo Secreto !!</p>" \
                  f"<br><h2>Você tirou: {nome} </h2><br>"\
                  f"<p>Sugestão de Presentes: {dados[2]}</p>" \
                  f"<p>Tenham uma Boa Confraternização!!</p>"

    msg = email.message.Message()
    msg['Subject'] = "Nome do Seu Amigo Secreto".upper()
    msg['From'] = "tec.mundo.py@gmail.com"
    msg['To'] = dados[1]
    password = 'jakhonuthvdvrkvw'
    msg.add_header('Content-Type', 'text/html' )
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg["from"], [msg["to"]], msg.as_string().encode("utf-8"))



