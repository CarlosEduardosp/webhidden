import random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import functions


# criando instancia do sqllite
# Cria a extensão
db = SQLAlchemy()

# criando o app, instancia do flask
app = Flask(__name__)

# criar  a chave secreta com o comando = import os ; print(os.urandom(16))
app.secret_key = "b'\xf5w\xa2z\x82V\xa6\\\x15\xf7\xa9n\xb4\xeaN\xb5'"

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# initialize the app with the extension
db.init_app(app)

def chave_estrangeira(nome_usuario):
    usuarios = db.session.execute(db.select(usuario)).all()
    for pessoas in usuarios:
        if nome_usuario == pessoas[0].nome:
            chave = pessoas[0].id
            return chave

def consultar_db():
    users = db.session.execute(db.select(user)).all()
    return users

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.Integer, unique=False, nullable=False)
    nome = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=False, nullable=False)
    obs = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, nome, email, obs, chave):
        self.nome = nome
        self.email = email
        self.obs = obs
        self.chave = chave

class usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=False, nullable=False)
    senha = db.Column(db.String, unique=False, nullable=False)


    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha


@app.route('/home/<nome_usuario>', methods=['GET', 'POST'])
def home(nome_usuario):

    # recebe o nome e o email do formulário
    if request.method == 'POST':
        nome = request.form.get('nome').title()
        email = request.form.get('email')
        obs = request.form.get('obs')
        if not obs:
            obs = 'Nenhuma sugestão foi digitada.'


        chave =chave_estrangeira(nome_usuario)


        #consulta ao banco de dados
        users = consultar_db()
        banco = user.query.filter_by(chave=chave).all()

        # consulta se o nome já existe no banco de dados
        resp = functions.validar_entrada(nome, email, banco)

        # resp True para nome que já consta no bd e resp False para email que já consta no bd.
        if resp == True:
            flash("Nome já consta na lista, digite o nome e o sobrenome, para diferenciar as pessoas!!", "error")
        elif resp == False:
            flash("Email já consta na lista, por favor digite um email diferente!!", "error")
        else:
            if request.method == 'POST':
                if not nome or not email :
                    flash("Preencha todos os campos do formulário!", "error")
                else:
                    # adicionando pessoas no banco de dados.

                    pessoa = user(nome, email, obs, chave)
                    db.session.add(pessoa)
                    db.session.commit()
                    flash(f"{nome.title()} já foi adicionado(a) a lista.")

    return render_template('home.html', nome_usuario=nome_usuario)


@app.route('/lista<nome_usuario>', methods=['GET','POST'])
def lista(nome_usuario):
    chave = chave_estrangeira(nome_usuario)


    users = consultar_db()
    lista = []
    for pessoas in users:
        if chave == pessoas[0].chave:
            lista.append(pessoas[0].nome)
            lista.append(pessoas[0].email)
            lista.append(pessoas[0].obs)

    # corpo do email para ser enviado para todos da lista.
    if request.method == 'POST':
        corpo_email = request.form.get('corpo_email')



    return render_template('lista.html', users=users, nome_usuario=nome_usuario, lista=lista, chave=chave)


@app.route('/sorteio/<nome_usuario>')
def sortear(nome_usuario):
    users = consultar_db()

    chave = chave_estrangeira(nome_usuario)

    users = user.query.filter_by(chave=chave).all()

    lista = users

    random.shuffle(lista)
    quantidade_pessoas_lista = len(lista)


    dados = []
    for pessoa in range(quantidade_pessoas_lista):
        if pessoa == quantidade_pessoas_lista - 1:
            nome = lista[pessoa].nome
            email = lista[pessoa].email
            obs = lista[pessoa - pessoa].obs
            nome_sorteado = lista[pessoa - pessoa].nome
            dados.append(nome)
            dados.append(email)
            dados.append(obs)
            dados.append(nome_sorteado)
            functions.enviar_email(dados)

        else:
            nome = lista[pessoa].nome
            email = lista[pessoa].email
            obs = lista[pessoa + 1].obs
            nome_sorteado = lista[pessoa + 1].nome
            dados.append(nome)
            dados.append(email)
            dados.append(obs)
            dados.append(nome_sorteado)
            functions.enviar_email(dados)
            dados = []
    flash('todos os Nomes e sugestões, foram Sorteados e Enviados por Email com sucesso.'.title())

    return render_template('sorteio.html',quantidade_pessoas_lista=quantidade_pessoas_lista,users=users,lista=lista, nome_usuario=nome_usuario)


@app.route('/<int:id>/deletar/<nome_usuario>', methods=['GET','POST'])
def deletar(id, nome_usuario):
        dados = user.query.filter_by(id=id).first()
        db.session.delete(dados)
        db.session.commit()
        return redirect(url_for('lista', nome_usuario=nome_usuario))


@app.route('/<int:id>/editar/<nome_usuario>', methods=["GET", "POST"])
def editar(id,nome_usuario):

    users = consultar_db()
    if request.method == 'POST':
        nome = request.form.get('nome').title()
        email = request.form.get('email')
        obs = request.form.get('obs')

        user.query.filter_by(id=id).update({"nome": nome, "email": email, "obs": obs})
        db.session.commit()
        return redirect(url_for('lista', nome_usuario=nome_usuario))
    return render_template('editar.html', users=users, id=id, nome_usuario=nome_usuario)



@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    cont = 0
    if request.method == 'POST':
        nome = request.form.get('nome').title()
        senha = request.form.get('password')
        usuarios = db.session.execute(db.select(usuario)).all()

    if nome and senha:
        for pessoas in usuarios:
            if nome == pessoas[0].nome:
                cont = 1
                break
            else:
                cont = 0


        if cont == 1:
            flash('Padrão já existente, favor digite outro')
        elif cont == 0:
            pessoa = usuario(nome, senha)
            db.session.add(pessoa)
            db.session.commit()
            mensagem = f'{nome}, Foi Cadastrado com Sucesso.'
            flash(mensagem)


    elif nome and not senha:
        mensagem = 'Por Favor Digite o Campo: SENHA'
        flash(mensagem)

    elif senha and not nome:
        mensagem = 'Por Favor Digite o Campo: NOME'
        flash(mensagem)

    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    nome = None
    senha = None
    if request.method == 'POST':
        nome = request.form.get('nome').title()
        senha = request.form.get('password')

    usuarios = db.session.execute(db.select(usuario)).all()
    mensagem = ''
    for pessoa in usuarios:
        if nome:
            if nome == pessoa[0].nome and senha == pessoa[0].senha:
                return redirect(url_for('home', nome_usuario=nome))
            elif nome != pessoa[0].nome or senha != pessoa[0].senha:
                mensagem = 'Usuário Inválido!! Ou Senha Incorreta!! Tente Outra Vez'
    flash(mensagem)

    return render_template('login.html')


@app.route('/contato/<nome_usuario>')
def contato(nome_usuario):
   return render_template('contato.html', nome_usuario=nome_usuario)

@app.route('/sugestao/<nome_usuario>', methods=['POST'])
def sugestao(nome_usuario):
    if request.method == 'POST':
        sugestao = request.form.get('sugestao')
        if sugestao:
            functions.enviar_sugestao(sugestao)
            flash('Sua Mensagem Foi Enviada com Sucesso!! Muito Obrigado!!')
        return redirect(url_for('contato', nome_usuario=nome_usuario))

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()