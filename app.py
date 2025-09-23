# Importando os arquivos
from flask import Flask, render_template, request, redirect, session
import datetime
import mysql.connector
from data.conexao import Conexao
from model.controllers.controler_usuario import Usuario

app = Flask(__name__)

# ------------------------------------------------------------------------------------------------------# 

# Rota para a página principal
@app.route("/")
def pagina_principal():

    return render_template("index.html")

@app.route("/pagina/cadastrar")
def pagina_cadastrar():

    return render_template("cadastro.html")

# Rota para a página de cadastro
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

app.run(debug = True)