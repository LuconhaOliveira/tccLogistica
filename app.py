# Importando os arquivos
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import datetime
import base64
from model.controllers.controller_usuario import Usuario
from model.controllers.controller_produtos import ControleProduto
from model.controllers.controler_estante import Estante
from model.controllers.controler_categorias import Categoria
from model.controllers.controller_historico import Historico
from model.controllers.controller_pedido import Pedido


app = Flask(__name__)

# Chave secreta para o funcionamento da sessão no Flask:
# Usada para criptografar os cookies de sessão (como 'cpf'), garantindo que os dados da sessão não possam ser lidos ou adulterados pelo usuário.
app.secret_key = "ch@v3s3cr3t4444&&@"

# PÁGINA PRINCIPAL ------------------------------------------------------------------------------------------------------#
 
# Rota para a página principal
@app.route("/principal")
def principal():

    if "cpf" not in session:
        return redirect(url_for('pagina_logar')) 
    
    else:
        nome = session['nome']
        return render_template("pagina_principal.html", nome=nome)

# FILTROS ------------------------------------------------------------------------------------------------------#

#API FILTRO
@app.route("/filtro")
def filtro():
    estantes = Estante.buscar_estantes()

    filtros=[]

    for i in estantes:
        filtros.append({"nome": i["categoria"],"cod_categoria": i["cod_categoria"]})


    return jsonify({"estantes": estantes,"filtros": filtros}), 200

#API FILTRO
@app.route("/filtro/<filtro>")
def filtro_filtro(filtro):
    estantes = Estante.buscar_estantes_filtro(filtro)

    filtros=[]

    for i in estantes:
        filtros.append({"nome": i["categoria"],"cod_categoria": i["cod_categoria"]})

    return jsonify({"estantes": estantes,"filtros": filtros}), 200

# CADASTRO DE USUÁRIO ------------------------------------------------------------------------------------------------------#
 
# Rota para a página de cadastro
@app.route("/cadastrar/usuario")
def cadastrar():

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
            "message": "Cadastro Feito!"
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

@app.route("/logoff", methods=['GET', 'POST'])
def logoff():
    Usuario.deslogar()
    return jsonify({"redirect": "/"}), 200

# Função da rota principal ("/") do aplicativo.

#    Esta rota é responsável por:
#    1. Lidar com a exibição da página de login.
#    2. Capturar e passar qualquer mensagem de erro para o template HTML.

@app.route("/")
def logar():

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
            "message": ""
        }), 200
    else:
        # Bloco executado se o login falhar

        # 3.3. Retorna a resposta de erro em formato JSON
        # Retorna uma resposta HTTP com status code 401 (Unauthorized - Não Autorizado)
        # e uma mensagem de erro.
        return jsonify({
            "status": "error",
            "message": "CPF ou senha inválidos. Tente novamente."
        }), 200

# RECUPERAR SENHA ------------------------------------------------------------------------------------------------------#
 
# Função da rota de recuperar senha do aplicativo.

# Esta rota é responsável por:
# 1. Lidar com a exibição da página de recuperar senha.
@app.route("/recuperar/senha")
def recuperar_senha():

    # 1. Renderiza o template HTML da página de recuperar senha.
    # 'render_template' carrega o arquivo 'pagina_recuperar_senha.html'.
    return render_template('pagina_recuperar_senha.html')

@app.route("/post/recuperar/senha", methods=["POST"])
def post_recuperar_senha():

    # 1. Captura os dados do formulário enviado via POST
    # Obtém o valor do campo 'login-cpf' do formulário
    cpf = request.form.get("login-cpf")
    # Obtém o valor do campo 'login-senha' do formulário
    nova_senha = request.form.get("login-senha")


    if not cpf or not nova_senha:
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
        Usuario.alterar_senha(cpf, nova_senha)

        # 4. Resposta de Sucesso.
        # Em caso de cadastro bem-sucedido, retorna o status HTTP 200 (OK)
        # e uma mensagem JSON que será usada pelo JavaScript (SweetAlert2) para notificar o usuário.
        return jsonify({
            "status": "success",
            "message": "Alteração realizada com sucesso!",
            "message": "Alteração realizada com sucesso!"
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
            "message": "Erro ao realizar a alteração. Tente novamente ou entre em contato."
        }), 500

# PRODUTOS ------------------------------------------------------------------------------------------------------#

# @app.route("/estante/<id>")
# def pagina_estante(id):

#     return jsonify(Estante.buscar_estante(id))
  
# Rota para exibir o formulário de cadastro de produto
@app.route("/cadastrar/produto")
def cadastrar_produto():
    """Renderiza o formulário para cadastro de novos produtos."""
    
    if "cpf" not in session:
        return redirect(url_for('pagina_logar')) 
    
    # Usuário está logado
    cpf = session["cpf"]
    
    # Tenta recuperar os dados dos selects (tratamento de erro seria ideal)
    categoria = Categoria.recuperar_categoria(cpf)
    tipo = Categoria.recuperar_tipo(cpf)
    caracteristica = Categoria.recuperar_caracteristica(cpf)
    estante = Estante.recuperar_estante(cpf)

    # Renderiza o template, passando os dados para os selects
    return render_template(
        "pagina_cadastrar_produto.html", 
        categoria=categoria, 
        tipo=tipo, 
        caracteristica=caracteristica, 
        estante=estante
    )

# CADASTRAR PRODUTOS ------------------------------------------------------------------------------------------------------#

# Rota de POST para cadastro de produto
# app.py (Rota /post/cadastrar/produto)
@app.route("/post/cadastrar/produto", methods=['POST'])
def post_produto():
    """
    Processa o formulário de cadastro de produto via AJAX e retorna JSON, 
    incluindo validação de campos OBRIGATÓRIOS.
    AGORA SUPORTA SELECT MULTIPLE PARA CARACTERÍSTICAS.
    """
    # 1. Verificação de Sessão
    if "cpf" not in session:
        return jsonify({
            'status': 'error', 
            'message': 'Sessão expirada. Por favor, faça login novamente.'
        })

    user_cpf = session["cpf"]
    
    # 2. Obter dados do formulário (incluindo campos NULÁVEIS)
    sku = request.form.get("cadastro-sku")
    descricao = request.form.get("cadastro-descricao")
    coluna = request.form.get("cadastro-coluna-estante")
    linha = request.form.get("cadastro-linha-estante")
    
    # Campos que serão validados como OBRIGATÓRIOS ou numéricos
    nome = request.form.get("cadastro-nome")
    quantidade_str = request.form.get("cadastro-quantidade")
    cod_tipo_str = request.form.get("cadastro-tipo") # cod_tipo é NOT NULL
    
    cod_estante = request.form.get("cadastro-nome-estante")
    cod_categoria = request.form.get("cadastro-categoria")
    
    # NOVO: Obtém a lista de IDs do SELECT MULTIPLE
    selected_caracteristicas_ids_str = request.form.getlist("cadastro-caracteristicas")


    # 3. Validação de Campos NOT NULL (Backend)
    try:
        # 3.1. NOME (NOT NULL)
        if not nome or nome.strip() == "":
            raise ValueError("O campo Nome do produto é obrigatório.")

        # 3.2. QUANTIDADE (NOT NULL e INT)
        if not quantidade_str or quantidade_str.strip() == "":
            raise ValueError("O campo Quantidade é obrigatório.")
            
        quantidade = int(quantidade_str)
        if quantidade < 0:
            raise ValueError("A Quantidade não pode ser negativa.")

        # 3.3. TIPO (cod_tipo é NOT NULL)
        if not cod_tipo_str:
            raise ValueError("A seleção do Tipo de produto é obrigatória.")
        cod_tipo = int(cod_tipo_str) 
        
        # 3.4. VALOR (Limpeza e conversão)
        valor_str_input = request.form.get("cadastro-valor", "0,00") # Pega o valor com máscara
        
        # Limpa: remove separador de milhar (.), troca vírgula por ponto (,)
        valor_clean = valor_str_input.replace('.', '').replace(',', '.')
        
        # Converte para float, usando 0.0 se estiver vazio após limpeza
        valor = float(valor_clean) if valor_clean else 0.0 

        # 3.5. Conversão dos outros IDs (NULÁVEIS)
        cod_estante = int(cod_estante) if cod_estante else None
        cod_categoria = int(cod_categoria) if cod_categoria else None
        
        # 3.6. Conversão das características (lista de strings para lista de inteiros)
        caracteristicas_ids = [int(cod) for cod in selected_caracteristicas_ids_str if cod.isdigit()]


    except (TypeError, ValueError) as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        })

    # 4. Validação da IMAGEM (NOT NULL)
    imagem_file = request.files.get("cadastro-imagem")
    imagem_blob = imagem_file.read() if imagem_file and imagem_file.filename else None

    if not imagem_blob:
        return jsonify({
            'status': 'error', 
            'message': 'A imagem do produto é obrigatória.'
        })

    # 5. CHAMA A FUNÇÃO DE CADASTRO
    # Note que agora 'caracteristicas_ids' é uma LISTA de IDs, e não mais um dicionário de valores.
    sucesso, mensagem_ou_id = ControleProduto.cadastrar_produto(
        nome, descricao, imagem_blob, quantidade, valor, sku,
        coluna, linha, cod_estante, cod_categoria,
        cod_tipo, user_cpf, caracteristicas_ids
    )

    # 6. Retorno JSON (mantém a lógica SweetAlert)
    if sucesso:
        return jsonify({
            'status': 'success',
            'message': f"Produto Cadastrado!" 
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f"Falha no cadastro (DB). Detalhes: {mensagem_ou_id}" 
        })

# EXCLUSÃO DE PRODUTO ------------------------------------------------------------------------------------------------------#  

# Rota para excluir um produto
@app.route("/post/produto/remover/<cod_produto>")
def remover_produto(cod_produto):
    cod_produto = int(cod_produto)
    # Chama a função do controler, remove a categoria e redireciona para a pagina de cadastro de categoria
    ControleProduto.remover_produto(cod_produto)

    return redirect("/principal")

# VIZUALIZAR PRODUTO ESPECIFICO ------------------------------------------------------------------------------------------------------#

@app.route("/visualizar/produto/<cod_produto>")
def visualizar_produto(cod_produto):
            
    cod_produto = int(cod_produto)

    produto = ControleProduto.selecionar_produto(cod_produto)

    if produto and produto.get('imagem'):
        imagem_blob = produto['imagem']
        imagem_base64 = base64.b64encode(imagem_blob).decode('utf-8')
        produto['imagem'] = f"data:image/jpeg;base64,{imagem_base64}"
    else:
        produto['imagem'] = None

    return render_template("pagina_visualizar_produto.html", produto = produto)# EDIÇÃO DE PRODUTO --------------------------------------------------------------------------------------------------------#  

@app.route("/pagina/editar/produto/<id>")
def editar_produto(id):
    produto = ControleProduto.buscar_produto(id)
    imagem_base64 = ""
    if produto["imagem"]:
        imagem_blob = produto["imagem"]  # Aqui o produto.imagem é o BLOB do banco de dados

        # Convertendo o BLOB para base64
        imagem_base64 = base64.b64encode(imagem_blob).decode('utf-8')

    caracteristicas = Categoria.recuperar_caracteristica(session["cpf"])
    tipos = Categoria.recuperar_tipo(session["cpf"])
    categorias = Categoria.recuperar_categoria(session["cpf"])
    estantes = Estante.buscar_estantes()
    print(produto)
    return render_template('pagina_editar_produto.html', produto=produto, caracteristicas=caracteristicas,tipos=tipos,categorias=categorias, estantes=estantes, imagem_base64=imagem_base64)

@app.route("/post/editar/produto/<id>", methods=["POST"])
def post_editar_produto(id):
    produto = ControleProduto.buscar_produto(id)
    # 1. Verificação de Sessão
    if "cpf" not in session:
        return jsonify({
            'status': 'error', 
            'message': 'Sessão expirada. Por favor, faça login novamente.'
        })
    
    # 2. Obter dados do formulário (incluindo campos NULÁVEIS)
    sku = request.form.get("cadastro-sku")
    descricao = request.form.get("cadastro-descricao")
    coluna = request.form.get("cadastro-coluna-estante")
    linha = request.form.get("cadastro-linha-estante")
    
    # Campos que serão validados como OBRIGATÓRIOS ou numéricosa
    quantidade_str = request.form.get("cadastro-quantidade",str(produto["quantidade"]))
    cod_tipo_str = request.form.get("cadastro-tipo") # cod_tipo é NOT NULL
    
    cod_estante = request.form.get("cadastro-nome-estante")
    cod_categoria = request.form.get("cadastro-categoria")
    cod_caracteristica = request.form.get("cadastro-caracteristicas")
    
    # 3. Validação de Campos NOT NULL (Backend)
    try:

        # 3.2. QUANTIDADE (NOT NULL e INT)
        if not quantidade_str or quantidade_str.strip() == "":
            raise ValueError("O campo Quantidade é obrigatório.")
            
        quantidade = int(quantidade_str)
        if quantidade < 0:
            raise ValueError("A Quantidade não pode ser negativa.")

        # 3.3. TIPO (cod_tipo é NOT NULL)
        if not cod_tipo_str:
            raise ValueError("A seleção do Tipo de produto é obrigatória.")
        cod_tipo = int(cod_tipo_str) # Converte para int após validação NOT NULL
        
        # 3.4. VALOR (NÃO é NOT NULL, mas a conversão é importante)
        valor_str = request.form.get("cadastro-valor").replace('.', '').replace(',', '.')
        valor = float(valor_str) if valor_str else 0.0 

        # 3.5. Conversão dos outros IDs (NULÁVEIS)
        cod_estante = int(cod_estante) if cod_estante else None
        cod_categoria = int(cod_categoria) if cod_categoria else None
        cod_caracteristica = int(cod_caracteristica) if cod_caracteristica else None


    except (TypeError, ValueError) as e:
        # Captura erros de validação personalizada (ValueError) e de conversão (TypeError)
        return jsonify({
            'status': 'error', 
            'message': str(e)
        })

    # 4. Validação da IMAGEM (NOT NULL)
    imagem_file = request.files.get("cadastro-imagem")
    imagem_blob = imagem_file.read() if imagem_file and imagem_file.filename else produto["imagem"]

    # if not imagem_blob:
    #     return jsonify({
    #         'status': 'error', 
    #         'message': 'A imagem do produto é obrigatória.'
    #     })

    # 5. Chamar a função de controle de produto
    sucesso, mensagem_ou_id = ControleProduto.editar_produto(
        descricao, imagem_blob, quantidade, valor, sku,
        coluna, linha, cod_estante, cod_categoria,
        cod_tipo, cod_caracteristica,id
    )

    # 6. Retorno JSON
    if sucesso:
        return redirect(f"/pagina/editar/produto/{id}")
    else:
        return jsonify({
            'status': 'error',
            'message': f"Falha no cadastro (DB). Detalhes: {mensagem_ou_id}" 
        })
    
# CADASTRO DE ESTANTE ------------------------------------------------------------------------------------------------------# 

# Rota que lida com a requisição GET para a página de cadastro de estantes.
# Acessa a URL "/pagina/cadastro_estante" e renderiza o arquivo HTML 'pagina_estante.html',
# exibindo o formulário de cadastro de estante para o usuário.  
@app.route("/cadastrar/estante")
def cadastrar_estante():

    if "cpf" in session:
        cpf = session["cpf"]
        nome = session['nome']
        categoria = Categoria.recuperar_categoria(cpf)

    return render_template("pagina_estante.html",nome=nome, categoria = categoria)


# Rota que processa os dados do formulário de cadastrar estante (requisição POST).
@app.route("/post/cadastrar/estante", methods=["POST"])
def adicionar_estante():
    
    cpf = session.get("cpf")
    if not cpf:
        return jsonify({
            "status": "error",
            "titulo": "Sessão Expirada",
            "mensagem": "Por favor, faça login novamente para continuar.",
            "redirect": "/pagina/login"
        }), 401

    nome = request.form.get("nome")
    cod_categoria = request.form.get("cod_categoria")

    if not nome or not cod_categoria:
        return jsonify({
            "status": "error",
            "titulo": "Campos Vazios",
            "mensagem": "Preencha o nome e selecione a categoria da estante."
        }), 400

    try:
        cod_categoria_int = int(cod_categoria)
        sucesso = Estante.cadastrar_estante(nome, cpf, cod_categoria_int)

        if sucesso:
            return jsonify({
                "status": "success",
                "mensagem": "Estante Criada!"
            }), 201
        else:
            return jsonify({
                "status": "error",
                "titulo": "Erro no Banco de Dados",
                "mensagem": "Não foi possível cadastrar a estante. Tente novamente."
            }), 500


    except ValueError:
        return jsonify({
            "status": "error",
            "titulo": "Erro de Formato",
            "mensagem": "O código da categoria é inválido."
        }), 400

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({
            "status": "error",
            "titulo": "Erro Inesperado",
            "mensagem": "Ocorreu um erro desconhecido no servidor."
        }), 500
    
# BUSCAR ESTANTE -------------------------------------------------------------------------------------------------------------------------------#

@app.route("/estante/<id>")
def estante_especifica(id):

    # Busca o nome da estante selecionada
    nome_estante = Estante.buscar_nome_estante(id) 

    produtos = Estante.buscar_estante(id)
    print(produtos)
    imagens_base64 = []
    # Vai renderizar pra pagina estantes
    if produtos:
        for produto in produtos:
            if produto["imagem"]:
                imagem_blob = produto["imagem"]  # Aqui o produto.imagem é o BLOB do banco de dados

                # Convertendo o BLOB para base64
                imagens_base64.append(base64.b64encode(imagem_blob).decode('utf-8'))

    # A correção está aqui:
    return render_template('pagina_consultar_produtos.html', produtos=produtos, imagens_base64=imagens_base64, cod_estante=id, nome_estante = nome_estante)
    
# EXCLUSÃO DE ESTANTE ------------------------------------------------------------------------------------------------------#

# Rota para excluir uma estante 
@app.route("/post/remover/estante/<cod_estante>")
def remover_estante(cod_estante):
    # Chama a função do controler, remove a estante e redireciona para a pagina principal
    Estante.remover_estante(cod_estante)
    return redirect("/principal")

# EDITAR ESTANTE -------------------------------------------------------------------------------------------------------

@app.route("/editar/estante/<cod_estante>")
def editar_estante():
    
    return render_template("pagina_editar_estante.html")
    
# CADASTRO DE CATEGORIA ------------------------------------------------------------------------------------------------------# 

# Rota que lida com a requisição GET para a página de cadastro de categoria, tipo e caracteristica.
# Acessa a URL "/pagina/cadastro_categoria" e renderiza o arquivo HTML 'pagina_categoria.html',
# exibindo os formulários de cadastro de categoria, tipo e caracteristica para o usuário.
@app.route("/cadastrar/categoria")
def cadastrar_categoria():

    if "cpf" in session:
        cpf = session["cpf"]
        nome = session['nome']
        categoria = Categoria.recuperar_categoria(cpf)
        tipo = Categoria.recuperar_tipo(cpf)
        caracteristica = Categoria.recuperar_caracteristica(cpf)

    return render_template("pagina_categoria.html",nome=nome, categoria = categoria, tipo = tipo, caracteristica = caracteristica)

# Rota que processa os dados do formulário de cadastrar categoria (requisição POST).
@app.route("/post/cadastrar/categoria", methods = ["POST"])
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
    
    return redirect("/cadastrar/categoria")

# Rota que processa os dados do formulário de cadastrar tipo (requisição POST).
@app.route("/post/cadastrar/tipo", methods = ["POST"])
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
    
    return redirect("/cadastrar/categoria")

# Rota que processa os dados do formulário de cadastrar caracteristica (requisição POST).
@app.route("/post/cadastrar/caracteristica", methods = ["POST"])
def post_cadastrar_caracteristica():

    cpf = session.get("cpf") 

    if not cpf:
        print("Acesso negado: CPF não encontrado na sessão.")
        # Retorna 401 Unauthorized
        return jsonify({"status": "error", "message": "Sessão expirada. Por favor, faça login novamente."}), 401 

    # Coleta de dados
    nome = request.form.get("nome")
    cod_tipo_str = request.form.get("cod_tipo") 
    
    if not nome or not cod_tipo_str:
        return jsonify({"status": "error", "message": "Nome da Característica e Tipo são obrigatórios."}), 400 

    try:
        cod_tipo = int(cod_tipo_str)
        
        # Chamada à função de cadastro (Assumindo que Categoria é o módulo correto)
        Categoria.cadastrar_tipo_caracteristica(nome, cod_tipo, cpf)
        
        # SUCESSO: Retorna um JSON com status 'success'
        return jsonify({
        "status": "success",
        "mensagem": "Cadastros Realizados!"
    }), 200

    except ValueError:
        return jsonify({"status": "error", "message": "O Código de Tipo deve ser um número válido."}), 400
    except Exception as e:
        # Captura outros erros (ex: do banco de dados)
        print(f"Erro ao cadastrar característica: {e}")
        return jsonify({"status": "error", "message": "Ocorreu um erro interno ao salvar os dados."}), 500

# EXCLUSÃO DE CATEGORIA, TIPO E CARACTERISTICA --------------------------------------------------------------------------------------------#

# Rota para excluir uma categoria
@app.route("/post/remover/categoria/<cod_categoria>")
def remover_categoria(cod_categoria):

    # Chama a função do controler, remove a categoria e redireciona para a pagina de cadastro de categoria
    Categoria.remover_categoria(cod_categoria)

    return redirect("/cadastrar/categoria")

# Rota para excluir um tipo
@app.route("/post/remover/tipo/<cod_tipo>")
def remover_tipo(cod_tipo):

    # Chama a função do controler, remove a categoria e redireciona para a pagina de cadastro de categoria
    Categoria.remover_tipo(cod_tipo)

    return redirect("/cadastrar/categoria")

# Rota para excluir uma caracteristica
@app.route("/post/remover/caracteristica/<cod_caracteristica>")
def remover_caracteristica(cod_caracteristica):
    """
    Exclui uma característica e lida com o redirecionamento ou erro de dependência.
    """
    
    Categoria.remover_caracteristica(cod_caracteristica) 

    return redirect("/cadastrar/categoria")

# RECUPERA O HISTÓRICO DE ALTERAÇÃO DOS PRODUTOS, ESTANTES E CATEGORIAS -----------------------------------------------------#

@app.route("/historico/alteracoes")
def historico_alteracao():

    # Se o CPF estiver na sessão.
    if "cpf" in session:
        cpf = session["cpf"]
        # Recupera todas as alterações realizadas.
        alteracoes = Historico.recuperar_historico_alteracoes(cpf)

    # Redireciona para a página de histórico de alterações, recuperando elas.
    return render_template("pagina_historico_alteracoes.html", alteracoes = alteracoes)

# EXCLUI O HISTÓRICO DE ALTERAÇÃO DOS PRODUTOS, ESTANTES E CATEGORIAS -----------------------------------------------------#

@app.route("/pagina/remover/historico/alteracoes", methods=['POST'])
def excluir_historico_alteracao():

    # Se o CPF estiver na sessão
    if "cpf" in session:
        cpf = session["cpf"]

        # Executa a função de exclusão
        Historico.excluir_historico_alteracoes(cpf)
        
        # Após a exclusão, redireciona o usuário para a mesma página que ele estava.
        return redirect("/historico/alteracoes")

    # Se não houver CPF na sessão, redireciona para a página de histórico 
    return redirect("/historico/alteracoes")

# PEDIDO DE COMPRA -------------------------------------------------------------------------------------------------------

# CRIAÇÃO E ADIÇÃO AO PEDIDO DE COMPRA ------------------------------------------------------------------------------------#

@app.route("/post/pedido/<cod_produto>", methods=['POST'])
def adicionar_produto_pedido(cod_produto):

    # Se o CPF estiver na sessão
    if "cpf" in session:
        quantidade=request.form.get('cadastro-quantidade')
        (ativo,cod_pedido)=Pedido.verificar_pedido_ativo()
        if not ativo:
            cod_pedido=Pedido.criar_pedido()
        print(ativo,cod_pedido,cod_produto,quantidade)
        Pedido.adicionar_ao_pedido(cod_pedido,cod_produto,quantidade)
        return redirect(url_for("principal"))


    # Se não houver CPF na sessão, redireciona para a página de login
    return redirect(url_for("pagina_logar"))


@app.route("/pedido/compra")
def pedido_compra():
    print(Pedido.verificar_pedido_ativo()[0])
    if Pedido.verificar_pedido_ativo()[0]:
        itens_pedido = Pedido.buscar_itens_pedido()
        quantidade=0
        subtotal=0
        for item in itens_pedido:
            quantidade+=item["quantidade"]
            subtotal+=item["valor"]*item["quantidade"]
            imagem_blob=item["imagem"]
            imagem_base64 = base64.b64encode(imagem_blob).decode('utf-8')
            item["imagem"]=imagem_base64
        cod_pedido=Pedido.verificar_pedido_ativo()[1]
        return render_template("pagina_pedido_compra.html", itens_pedido=itens_pedido, quantidade=quantidade, subtotal=subtotal, cod_pedido=cod_pedido)
    else:
        return render_template("pagina_pedido_compra.html")

# EXCLUSÃO DE PRODUTO DO PEDIDO DE COMPRA ------------------------------------------------------------------------------------#

@app.route("/post/remover/produto/pedido/<cod_produto>")
def remover_produto_pedido(cod_produto):

    # Se o CPF estiver na sessão
    if "cpf" in session:
        Pedido.remover_produto(cod_produto)
        return redirect(url_for("pedido_compra"))


    # Se não houver CPF na sessão, redireciona para a página de login
    return redirect(url_for("pagina_logar"))

# FINALIZAR PEDIDO ------------------------------------------------------------------------------------#

@app.route("/post/finalizar/pedido/<cod_pedido>")
def finalizar_pedido(cod_pedido):

    # Se o CPF estiver na sessão
    if "cpf" in session:
        Pedido.remover_pedido(cod_pedido)
        return redirect(url_for("nota_fiscal"))


    # Se não houver CPF na sessão, redireciona para a página de login
    return redirect(url_for("pagina_logar"))

# HISTÓRICO DO PEDIDO DE COMPRA -------------------------------------------------------------------------------------------------------

@app.route("/historico/pedido/compra")
def historico_pedido_compra():

    return render_template("pagina_historico_pedido.html")

# NOTA FISCAL -------------------------------------------------------------------------------------------------------

@app.route("/nota/fiscal")
def nota_fiscal():
    
    return render_template("pagina_nota_fiscal.html")
# ----------------------------------------------------------------------------------------------------------------------------# 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)