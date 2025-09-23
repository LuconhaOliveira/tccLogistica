# Importando os arquivos
from flask import Flask, render_template, request, redirect, session
import datetime
import mysql.connector
from data.conexao import Conection
from model.controllers.controler_usuario import Usuario

app = Flask(__name__)

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
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)