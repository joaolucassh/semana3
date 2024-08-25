from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://joaolucassh.mysql.pythonanywhere-services.com:3306/joaolucassh$mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key= 'power123'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'view'

class Usuario(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    nome = db.Column('Nome', db.String(256))
    email = db.Column('Email', db.String(256))
    senha = db.Column('Senha', db.String(256))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Vendas(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    nome = db.Column('Nome', db.String(256))
    valor = db.Column('Valor', db.Integer)
    quant = db.Column('quant', db.Integer)
    descr = db.Column('descr', db.String(256))

    def __init__(self, id, nome, valor, quant, descr):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.quant = quant
        self.descr = descr

class Anuncio(db.Model):
    idcompra = db.Column('ID', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(256))
    preco = db.Column('preco', db.Integer)
    desc = db.Column('descricao', db.String(256))

    def __init__(self, idcompra, nome, preco, desc):
        self.idcompra = idcompra
        self.nome = nome
        self.preco = preco
        self.desc = desc

@app.errorhandler(404)
def erropagina(error):
    return render_template('erro.html')

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/")
def inicial():
    return render_template('inicial.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(email=email, senha=senha).first()

        if user:
            login_user(user)
            return redirect(url_for('inicial'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('inicial'))

@app.route("/usuario")
def usuario():
    return render_template('usuario.html')

@app.route("/anuncios")
def anuncios():
    return render_template('anuncios.html')

@app.route("/usuario/cadastro")
def cadastro():
    return render_template('cadastro.html')

@app.route("/usuario/caduser", methods=['POST'])
def caduser():
    hash = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('nome'), request.form.get('email'),hash)
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadastro'))

@app.route("/usuario/perfil/<int:id>")
def perfiluser(id):
    usuario = Usuario.query.get(id)
    return render_template('perfil.html', usuario=usuario)

 

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editaruser(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('name')
        usuario.email = request.form.get('email')
        usuario.senha = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
        return redirect(url_for('cadastro'))
    
    return render_template('edicaouser.html', usuario = usuario, titulo="Usuario")

@app.route("/usuario/delete/<int:id>")
def deleteuser(id):
    usuario = Usuario.query.get(id) 
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/anuncios/cadastro")
def criaranuncio():
    return render_template('cadanuncio.html')


@app.route("/anuncios/criar")
def cadanuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('preco'), request.form.get('desc'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('criaranuncio'))

@app.route("/relatorios")
def relatorio():
    return render_template('relatorios.html')

@app.route("/relatorio/vendas")
def vendas():
    return render_template('vendas.html')

@app.route("/relatorio/compras")
def compras():
    return render_template('compras.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
