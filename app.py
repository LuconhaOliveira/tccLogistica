# Importando os arquivos
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import datetime
from model.controllers.controller_usuario import Usuario
from model.controllers.controller_produtos import ControleProduto
from model.controllers.controler_estante import Estante

app = Flask(__name__)

# Chave secreta para o funcionamento da sessão no Flask:
# Usada para criptografar os cookies de sessão (como 'cpf'), garantindo que os dados da sessão não possam ser lidos ou adulterados pelo usuário.
app.secret_key = "ch@v3s3cr3t4444&&@"

# PÁGINA PRINCIPAL ------------------------------------------------------------------------------------------------------# 

# Rota para a página principal
@app.route("/pagina/principal")
def pagina_principal():
    session["cpf"] = "11223344556"
    estantes = Estante.buscar_estantes()

    filtros = [i["categoria"] for i in estantes]
    filtros = list(set(filtros))

    return render_template("pagina-principal.html",estantes=estantes,filtros=filtros)

# CADASTRO ------------------------------------------------------------------------------------------------------# 


# Rota para a página de cadastro
@app.route("/pagina/cadastrar")
def pagina_cadastrar():

    return render_template("tela-cadastro.html")

@app.route("/post/cadastro", methods = ["POST"])
def post_cadastro():

    cpf = request.form.get("cadastro-cpf")

    nome = request.form.get("cadastro-nome")

    senha = request.form.get("cadastro-senha")

    Usuario.cadastrar_usuario(cpf, nome, senha)
    
    return redirect("/pagina/login")

# LOGIN ------------------------------------------------------------------------------------------------------# 

@app.route("/logoff")
def logoff():
    Usuario.deslogar()
    return jsonify({"redirect": "/pagina/login"}), 200


# Rota que lida com a requisição GET para a página de login.
# Acessa a URL "/pagina_login" e renderiza o arquivo HTML 'pagina_login.html',
# exibindo o formulário de login para o usuário.
@app.route("/")
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
        session['cpf'] = cpf
        session['nome'] = login_valido

        # Se o login for bem-sucedido, redireciona para a página principal
        return render_template('index.html')
    else:
        # Se falhar, redireciona para a página de login com uma mensagem de erro
        return redirect(url_for('pagina_logar'))


@app.route("/estante/<id>")
def pagina_estante(id):
    Estante.buscar_estante(id)

    return render_template('pagina_estantes.html')
  
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

    
# CADASTRO DE ESTANTE ------------------------------------------------------------------------------------------------------# 

# Rota que lida com a requisição GET para a página de cadastro de estantes.
# Acessa a URL "/pagina/cadastro_estante" e renderiza o arquivo HTML 'pagina_estante.html',
# exibindo o formulário de cadastro de estante para o usuário.  
@app.route("/pagina/cadastro_estante")
def pagina_cadastrar_estante():

    return render_template('pagina_estante.html')


# Rota que processa os dados do formulário de cadastrar estante (requisição POST).
@app.route("/post/cadastro_estante/adicionar", methods=["POST"])
def adicionar_estante():
    
    # Usa .get() para evitar KeyError. Se o 'cpf' não existir, ele será None.
    cpf = session.get("cpf") 

    # Caso o CPF não estiver na sessão
    if not cpf:
        # nega o acesso e redireciona para o login, mostrando o erro no terminal.
        print("Acesso negado: CPF não encontrado na sessão.")
        return redirect("/pagina/login") 
    
    # Coleta de dados (só pega os dados se o CPF existir)
    enderecamento = request.form.get("enderecamento")
    estante = request.form.get("estante")
    linha = request.form.get("linha")
    coluna = request.form.get("coluna")
    cod_categoria = request.form.get("cod_categoria")

    # Garante que o campo 'cod_categoria' foi preenchido. 
    if not cod_categoria: 
        return redirect("/pagina/cadastro_estante") 
        
    # Inserção dos dados no Banco caso esteja tudo certo
    try:
        sucesso = Estante.cadastrar_estante(
            enderecamento, 
            estante, 
            linha, 
            coluna, 
            cpf, 
            int(cod_categoria)
        )
        
        if sucesso:
            # Caso a inserção de dados seja um sucesso, redireciona para a página principal (futuramente vai aparecer um sweet alert)
            return redirect(f"/estante/{cod_categoria}") 
        else:
            # Falha no banco de dados (erro interno na classe Estante)
            print(f"Erro no cadastro do banco de dados: {e}")
            return redirect("/pagina/cadastro_estante") 

    except ValueError: 
        # Erro de formato (se cod_categoria não for um número)
        print(f"Erro de valor invalido: {e}")
        return redirect("/pagina/cadastro_estante")
        
    except Exception as e:
        # Erro genérico de sistema
        print(f"Erro inesperado durante a persistência: {e}")
        return redirect("/pagina/cadastro_estante")
# ------------------------------------------------------------------------------------------------------# 

app.run(debug = True)
