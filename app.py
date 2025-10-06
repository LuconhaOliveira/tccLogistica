# Importando os arquivos
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import datetime
from model.controllers.controller_usuario import Usuario
from model.controllers.controller_produtos import ControleProduto
from model.controllers.controler_estante import Estante
from model.controllers.controler_categorias import Categoria

app = Flask(__name__)

# Chave secreta para o funcionamento da sessão no Flask:
# Usada para criptografar os cookies de sessão (como 'cpf'), garantindo que os dados da sessão não possam ser lidos ou adulterados pelo usuário.
app.secret_key = "ch@v3s3cr3t4444&&@"

# PÁGINA PRINCIPAL ------------------------------------------------------------------------------------------------------# 

# Rota para a página principal
@app.route("/pagina/principal")
def pagina_principal():
    estantes = Estante.buscar_estantes()

    if estantes is None:
        estantes = []

    filtros = [i["categoria"] for i in estantes]
    filtros = list(set(filtros))

    return render_template("index.html",estantes=estantes,filtros=filtros)


#API FILTRO
@app.route("/filtro")
def filtro():
    estantes = Estante.buscar_estantes()

    filtros = [i["categoria"] for i in estantes]
    filtros = list(set(filtros))


    return jsonify({"estantes": estantes,"filtros": filtros}), 200

#API FILTRO
@app.route("/filtro/<filtro>")
def filtro_filtro(filtro):
    estantes = Estante.buscar_estantes_filtro(filtro)

    filtros = [i["categoria"] for i in estantes]
    filtros = list(set(filtros))

    return jsonify({"estantes": estantes,"filtros": filtros}), 200

# CADASTRO ------------------------------------------------------------------------------------------------------# 

# Rota para a página de cadastro
@app.route("/pagina/cadastrar")
def pagina_cadastrar():

    return render_template("pagina_cadastro.html")

@app.route("/post/cadastro", methods = ["POST"])
def post_cadastro():

    """
    Rota de API (Endpoint POST) responsável por processar a submissão do formulário de cadastro.
    Esta rota segue o padrão de arquitetura REST, retornando respostas em formato JSON
    para serem tratadas de forma assíncrona (AJAX) pelo frontend.
    
    1. Coleta os dados (CPF, nome e senha) enviados pelo formulário via requisição POST.
    """
    cpf = request.form.get("cadastro-cpf")
    nome = request.form.get("cadastro-nome")
    senha = request.form.get("cadastro-senha")

    # 2. Validação de dados de entrada (Input Validation).
    # Verifica se todos os campos obrigatórios foram preenchidos.
    # Em caso de falha, retorna um status HTTP 400 (Bad Request),
    # informando o frontend para exibir a mensagem de erro ao usuário.
    if not cpf or not nome or not senha:
        return jsonify({
            "status": "error",
            "message": "Todos os campos são obrigatórios."
        }), 400

    try:
        # 3. Execução da Lógica de Negócio.
        # Chama o método 'cadastrar_usuario' do modelo 'Usuario'.
        # Espera-se que este método execute o hash da senha (segurança) e o INSERT no banco de dados.
        # A responsabilidade de limpeza do CPF (remoção de pontos/traços) é delegada a este método,
        # mantendo a rota limpa e focada no controle de fluxo.
        Usuario.cadastrar_usuario(cpf, nome, senha)

        # 4. Resposta de Sucesso.
        # Em caso de cadastro bem-sucedido, retorna o status HTTP 200 (OK)
        # e uma mensagem JSON que será usada pelo JavaScript (SweetAlert2) para notificar o usuário.
        return jsonify({
            "status": "success",
            "message": "Cadastro realizado com sucesso! Faça login para continuar."
        }), 200
    
    except Exception as e:
        # 5. Tratamento de Exceções.
        # Este bloco captura erros que podem ocorrer na camada de acesso ao banco de dados (DAO),
        # como a tentativa de inserir um CPF duplicado (violação de chave primária) ou falhas de conexão.
        print(f"Erro ao cadastrar usuário: {e}") 

        # Retorna o status HTTP 500 (Internal Server Error) para indicar um erro do servidor/sistema,
        # garantindo que o frontend receba um código de erro apropriado para o tratamento.
        return jsonify({
            "status": "error",
            "message": "Erro ao realizar o cadastro. Tente novamente ou entre em contato."
        }), 500

# LOGIN ------------------------------------------------------------------------------------------------------# 

@app.route("/logoff")
def logoff():
    Usuario.deslogar()
    return jsonify({"redirect": "/pagina/login"}), 200


# Função da rota principal ("/") do aplicativo.

#    Esta rota é responsável por:
#    1. Lidar com a exibição da página de login.
#    2. Capturar e passar qualquer mensagem de erro para o template HTML.
@app.route("/")
def pagina_logar():

    # 1. Renderiza o template HTML da página de login.
    # 'render_template' carrega o arquivo 'pagina_login.html'.
    return render_template('pagina_login.html')
    



#    Função da rota responsável por processar o formulário de login (método POST).
#    Ela recebe o CPF e a senha do formulário, tenta validar as credenciais
#    e retorna uma resposta JSON (sucesso ou erro) para o cliente.
@app.route("/post/login", methods=["POST"])
def post_login():
    # 1. Captura os dados do formulário enviado via POST
    # Obtém o valor do campo 'login-cpf' do formulário
    cpf = request.form.get("login-cpf")
    # Obtém o valor do campo 'login-senha' do formulário
    senha = request.form.get("login-senha")

    if not cpf or not senha:
        return jsonify({
            "status": "error",
            "message": "Todos os campos são obrigatórios."
        }), 400
    
    # 2. Chama a lógica de validação de login
    # Chama a função estática ou de classe 'validar_login' do modelo 'Usuario'.
    # Espera-se que esta função:
    # - Retorne o NOME do usuário se o login for válido.
    # - Retorne um valor False/None se o login for inválido.
    nome_usuario, cpf_limpo = Usuario.validar_login(cpf, senha)

    # 3. Processa o resultado da validação
    if nome_usuario:
        # Bloco executado se o login for bem-sucedido (login_valido contém o nome)

        # 3.1. Gerencia a sessão do usuário
        # Armazena o CPF na sessão do Flask (mantendo o usuário logado)
        session['cpf'] = cpf_limpo
        # Armazena o NOME do usuário na sessão para exibição
        session['nome'] = nome_usuario

        # 3.2. Retorna a resposta de sucesso em formato JSON
        # Retorna uma resposta HTTP com status code 200 (OK) e uma mensagem de sucesso
        return jsonify({
            "status": "success",
            "message": f"Login realizado com sucesso! Bem-vindo(a), {nome_usuario}."
        }), 200
    else:
        # Bloco executado se o login falhar

        # 3.3. Retorna a resposta de erro em formato JSON
        # Retorna uma resposta HTTP com status code 401 (Unauthorized - Não Autorizado)
        # e uma mensagem de erro.
        return jsonify({
            "status": "error",
            "message": "CPF ou senha inválidos. Tente novamente."
        }), 401


@app.route("/estante/<id>")
def pagina_estante(id):
    print(Estante.buscar_estante(id))

    return redirect(url_for('pagina_logar'))
  
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

    categoria = Categoria.recuperar_categoria()

    return render_template("pagina_estante.html", categoria = categoria)


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
    nome = request.form.get("nome")
    cod_categoria = request.form.get("cod_categoria")

    # Garante que o campo 'cod_categoria' foi preenchido. 
    if not cod_categoria: 
        return redirect("/pagina/cadastro_estante") 
        
    # Inserção dos dados no Banco caso esteja tudo certo
    try:
        sucesso = Estante.cadastrar_estante(
            nome,
            cpf, 
            int(cod_categoria)
        )
        
        if sucesso:
            # Caso a inserção de dados seja um sucesso, redireciona para a página principal (futuramente vai aparecer um sweet alert)
            return redirect("/pagina/principal") 
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
    
# CADASTRO DE CATEGORIA ------------------------------------------------------------------------------------------------------# 

# Rota que lida com a requisição GET para a página de cadastro de categoria, tipo e caracteristica.
# Acessa a URL "/pagina/cadastro_categoria" e renderiza o arquivo HTML 'pagina_categoria.html',
# exibindo os formulários de cadastro de categoria, tipo e caracteristica para o usuário.
@app.route("/pagina/cadastrar/categoria")
def pagina_cadastrar_categoria():

    categoria = Categoria.recuperar_categoria()
    tipo = Categoria.recuperar_tipo()

    return render_template("pagina_categoria.html", categoria = categoria, tipo = tipo)

# Rota que processa os dados do formulário de cadastrar categoria (requisição POST).
@app.route("/post/cadastro_categoria/adicionar", methods = ["POST"])
def post_cadastrar_categoria():

    # Usa .get() para evitar KeyError. Se o 'cpf' não existir, ele será None.
    cpf = session.get("cpf") 

    # Caso o CPF não estiver na sessão
    if not cpf:
        # nega o acesso e redireciona para o login, mostrando o erro no terminal.
        print("Acesso negado: CPF não encontrado na sessão.")
        return redirect("/pagina/login") 
    
    # Coleta de dados (só pega os dados se o CPF existir)
    nome = request.form.get("nome")

    Categoria.cadastrar_categoria(nome, cpf)
    
    return redirect("/pagina/cadastrar/categoria")

# Rota que processa os dados do formulário de cadastrar tipo (requisição POST).
@app.route("/post/cadastro_tipo/adicionar", methods = ["POST"])
def post_cadastrar_tipo():

    # Usa .get() para evitar KeyError. Se o 'cpf' não existir, ele será None.
    cpf = session.get("cpf") 

    # Caso o CPF não estiver na sessão
    if not cpf:
        # nega o acesso e redireciona para o login, mostrando o erro no terminal.
        print("Acesso negado: CPF não encontrado na sessão.")
        return redirect("/pagina/login") 
    
    # Coleta de dados (só pega os dados se o CPF existir)
    nome = request.form.get("nome")
    cod_categoria = request.form.get("cod_categoria")
    

    Categoria.cadastrar_tipo_categoria(nome, cpf, int(cod_categoria))
    
    return redirect("/pagina/cadastrar/categoria")

# Rota que processa os dados do formulário de cadastrar caracteristica (requisição POST).
@app.route("/post/cadastro_caracteristica/adicionar", methods = ["POST"])
def post_cadastrar_caracteristica():

    # Usa .get() para evitar KeyError. Se o 'cpf' não existir, ele será None.
    cpf = session.get("cpf") 

    # Caso o CPF não estiver na sessão
    if not cpf:
        # nega o acesso e redireciona para o login, mostrando o erro no terminal.
        print("Acesso negado: CPF não encontrado na sessão.")
        return redirect("/pagina/login") 
    
    # Coleta de dados (só pega os dados se o CPF existir)
    nome = request.form.get("nome")
    cod_tipo = request.form.get("cod_tipo")
    
    Categoria.cadastrar_tipo_caracteristica(nome, int(cod_tipo), cpf)
    
    return redirect("/pagina/cadastrar/categoria")

# RECUPERAR CATEGORIA,TIPO E CARACTERISTICA ------------------------------------------------------------------------------------------------------# 


# ------------------------------------------------------------------------------------------------------# 

app.run(debug = True)
