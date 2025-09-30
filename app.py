# Importando os arquivos
from flask import Flask, jsonify, render_template, request, redirect, session
import datetime
import mysql.connector
from data.conexao import Conection
from model.controllers.controler_usuario import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teste123'

# ------------------------------------------------------------------------------------------------------# 

# Rota para a página principal
# @app.route("/")
# def pagina_principal():

#     return render_template("index.html")

# Rota para a página de cadastro
@app.route("/pagina/cadastrar")
def pagina_cadastrar():

    return render_template("cadastro.html")

@app.route("/post/cadastro", methods = ["POST"])
def post_cadastro():

    cpf = request.form.get("cadastro-cpf")

    nome = request.form.get("cadastro-nome")

    senha = request.form.get("cadastro-senha")

    # if Usuario.verificar_usuario_existente(cpf):
    #     return redirect("/pagina/cadastrar")

    # else: 
    Usuario.cadastrar_usuario(cpf, nome, senha)
    
    return redirect("/pagina/login")

@app.route("/")
def ipsum():
    return render_template("lorem-ipsum.html")

@app.route("/logoff")
def logoff():
    Usuario.deslogar()
    return jsonify({"redirect": "/login"}), 200

@app.route("/login")
def login():
    return render_template("login.html")

