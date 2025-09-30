# Importando os arquivos
from flask import Flask, jsonify, render_template, request, redirect, session
import datetime
from model.controllers.controler_usuario import Usuario
from model.controllers.controller_estante import Estante

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teste123'

# ------------------------------------------------------------------------------------------------------# 

# Rota para a página principal
@app.route("/")
def pagina_principal():
    session["cpf"] = "11223344556"
    estantes = Estante.buscar_estantes()

    filtros = [i["categoria"] for i in estantes]
    filtros = list(set(filtros))

    return render_template("index.html",estantes=estantes,filtros=filtros)

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


@app.route("/logoff")
def logoff():
    Usuario.deslogar()
    return jsonify({"redirect": "/"}), 200


# Rota que lida com a requisição GET para a página de login.
# Acessa a URL "/pagina_login" e renderiza o arquivo HTML 'pagina_login.html',
# exibindo o formulário de login para o usuário.
@app.route("/pagina/login")
def pagina_logar():

    return render_template('pagina_login.html')
    
# Rota que processa os dados do formulário de login (requisição POST).
# Esta função:
# 1. Recebe o CPF e a senha enviados pelo formulário.
# 2. Chama a função 'validar_login' da classe 'Usuario' para verificar as credenciais no banco de dados.
# 3. Usa uma condicional 'if' para verificar o resultado da validação.
#    - Se o login for bem-sucedido ('login_valido' é True), ela renderiza a página 'pagina_principal.html'.
#    - Se o login falhar, redireciona o usuário de volta para a página de login para que ele possa tentar novamente.
@app.route("/post/login", methods=["POST"])
def post_login():
    cpf = request.form.get("login-cpf")
    senha = request.form.get("login-senha")
    
    # Chama a função para validar o login
    login_valido = Usuario.validar_login(cpf, senha)

    if login_valido:
        # Se o login for bem-sucedido, redireciona para a página principal
        return render_template('pagina_principal.html')
    else:
        # Se falhar, redireciona para a página de login com uma mensagem de erro
        return redirect("/pagina/login")

@app.route("/estante/<id>")
def pagina_logar(id):
    Estante.buscar_estante(id)
    
    return render_template('pagina_login.html')

