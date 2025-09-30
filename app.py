# Importando os arquivos
from flask import Flask, jsonify, render_template, request, redirect, session
import datetime
from model.controllers.controller_usuario import Usuario
from model.controllers.controller_produtos import ControleProduto

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teste123'

# ------------------------------------------------------------------------------------------------------# 

# Rota para a página principal
@app.route("/")
def pagina_principal():

    # return render_template("index.html")
    return render_template('pagina_login.html')

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
    return jsonify({"redirect": "/login"}), 200


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



# Rota para exibir o formulário de cadastro de produto
@app.route("/pagina/produto")
def pagina_produto():
    """Renderiza o formulário para cadastro de novos produtos."""

    return render_template('cadastro_produto.html') 

# Rota de POST para cadastro de produto
@app.route("/post/produto", methods=["POST"])
def post_produto():
    """
    Processa o formulário de cadastro de produto, incluindo o upload da imagem.
    """
    # 1. Obter dados do formulário
    cpf = request.form.get("cadastro-cpf")
    sku = request.form.get("cadastro-sku")
    descricao = request.form.get("cadastro-descricao")
    nome = request.form.get("cadastro-nome")
    
    # É crucial converter o valor e o cod_tipo para os tipos numéricos corretos
    try:
        valor = float(request.form.get("cadastro-valor"))
        cod_tipo = int(request.form.get("cadastro-cod_tipo"))
    except (TypeError, ValueError):
        print("Erro: Valor ou Cód. Tipo não são números válidos.")
        # Retornaria uma mensagem de erro ao usuário
        return redirect("/pagina/produto") 
    
    # 2. Obter o arquivo de imagem
    # Request.files para acessar arquivos carregados
    imagem_file = request.files.get("cadastro-imagem") 

    # 3. Chamar a função de controle de produto
    sucesso = ControleProduto.cadastrar_produto(
        cpf, sku, imagem_file, descricao, nome, valor, cod_tipo
    )

    if sucesso:
        # Redireciona para alguma página de confirmação ou lista de produtos
        return redirect("/pagina/principal") 
    else:
        # Redireciona de volta com erro
        return redirect("/pagina/produto") 
    

@app.route("/post/deletar_produto", methods=["POST"])
def post_deletar_produto():
    """
    Processa a exclusão de um produto, recebendo o cod_produto via POST.
    """
    try:
        cod_produto = int(request.form.get("cod_produto"))
    except (TypeError, ValueError):
        # Se o código do produto não for um número válido, retorna erro
        return "Erro: Código do produto inválido.", 400

    # Chama a função de exclusão
    sucesso = ControleProduto.deletar_produto(cod_produto)

    if sucesso:
        # Redireciona de volta para a lista de produtos após a exclusão
        return redirect("/pagina/listagem_produtos")
    else:
        # Em caso de falha (erro de BD ou produto não encontrado)
        return "Erro ao deletar o produto. Verifique dependências.", 500


app.run(debug = True)
