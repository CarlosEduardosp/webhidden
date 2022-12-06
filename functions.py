from flask_sqlalchemy import SQLAlchemy
import  random
import smtplib
import email.message



def validar_entrada(nome, email, banco):
    for pessoa in banco:
        if nome == pessoa.nome:
            return True
        elif email == pessoa.email:
            return False
        else:
            return 'nada'


#função para envio de emails sorteados.
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


# função para o envio de emails de sugestão
def enviar_sugestao(sugestao):
    corpo_email = f"<p>{sugestao}</p>"

    msg = email.message.Message()
    msg['Subject'] = "Hidden - Alguém te enviou uma Sugestão.".upper()
    msg['From'] = "tec.mundo.py@gmail.com"
    msg['To'] = 'carlos.spadilha@yahoo.com.br'
    password = 'jakhonuthvdvrkvw'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg["from"], [msg["to"]], msg.as_string().encode("utf-8"))


