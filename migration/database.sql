-- =========================================================================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS PARA O PROJETO TCC: GESTÃO LOGÍSTICA DE ESTOQUE E PEDIDOS
-- AUTOR: [Gabriel Belentani Felipe / Lucas Oliveira da Silva / Eduarda Cristina Virgilio]
-- DATA: [30/09/2025]
-- =========================================================================================================

-- Cria e utiliza o banco de dados principal do sistema de gestão logística.
CREATE DATABASE IF NOT EXISTS tcc_logistica;
USE tcc_logistica;

-- =========================================================================================================
-- LIMPEZA (DROP TABLES)
-- NECESSÁRIO para garantir que não haja tabelas antigas que causem erros de Foreign Key (Erro 1822).
-- As tabelas são excluídas na ordem inversa de suas dependências.
-- =========================================================================================================
DROP TABLE IF EXISTS item_pedido;
DROP TABLE IF EXISTS armazenamento;
DROP TABLE IF EXISTS produto_caracteristica;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS caracteristica;
DROP TABLE IF EXISTS alteracao_produto_estante;
DROP TABLE IF EXISTS estante;
DROP TABLE IF EXISTS tipo;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS usuario;

-- ---------------------------------------------------------------------------------------------------------
-- 1. TABELA USUARIO
-- Propósito: Autenticação e autorização de acesso ao sistema. O CPF é utilizado como identificador principal.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
    -- Chave primária: Cadastro de Pessoa Física (CPF), fixado em 11 caracteres.
    cpf VARCHAR(14) PRIMARY KEY NOT NULL,
    -- Nome completo do usuário.
    nome VARCHAR(100),
    -- Senha criptografada (hash). Usa VARCHAR(255) para armazenar o hash SHA-256 (ou similar).
    senha VARCHAR(255)
);

-- ---------------------------------------------------------------------------------------------------------
-- 2. TABELA CATEGORIA
-- Propósito: Armazenar as categorias gerais de produtos (ex: Eletrônicos, Alimentos, Ferramentas).
-- Define o topo da hierarquia de produtos.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categoria (
    -- Chave primária: Identificador único e sequencial da categoria.
    cod_categoria INT PRIMARY KEY AUTO_INCREMENT,
    -- Nome da categoria. Utiliza VARCHAR(100) para flexibilidade.
    nome VARCHAR(100),
    -- Data e hora que a categoria foi cadastrada.
    data_hora DATETIME NOT NULL,
	-- Chave estrangeira: Vincula a alteração ao usuário responsável.
    cpf VARCHAR(14) NOT NULL,
    FOREIGN KEY (cpf) REFERENCES usuario (cpf)
);

-- ---------------------------------------------------------------------------------------------------------
-- 3. TABELA TIPO
-- Propósito: Detalhar os tipos de produtos dentro de uma categoria (ex: Laptops, Smartphones, dentro de Eletrônicos).
-- Possui uma chave estrangeira para estabelecer a relação de 1:N com 'categoria'.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tipo (
    -- Chave primária: Identificador único e sequencial do tipo.
    cod_tipo INT PRIMARY KEY AUTO_INCREMENT,
    -- Nome do tipo.
    nome VARCHAR(100),
    -- Data e hora que o tipo foi cadastrado.
    data_hora DATETIME NOT NULL,
    -- Chave estrangeira: Vincula o tipo à sua categoria e ao usuário.
	cpf VARCHAR(14) NOT NULL, 
    FOREIGN KEY (cpf) REFERENCES usuario (cpf),
    cod_categoria INT,
    FOREIGN KEY (cod_categoria) REFERENCES categoria (cod_categoria)
);

-- ---------------------------------------------------------------------------------------------------------
-- 4. TABELA ALTERACAO_PRODUTO_ESTANTE
-- Propósito: Manter um registro (log de auditoria) de todas as alterações relevantes de estoque/endereçamento.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS alteracao_produto_estante (
    -- Chave primária: Identificador único do registro de alteração.
    cod_alteracao INT PRIMARY KEY AUTO_INCREMENT,
    -- Descrição detalhada da alteração realizada.
    alteracao_realizada VARCHAR(255),
    -- Data e hora que a alteração foi registrada.
    data_hora DATETIME NOT NULL,
    -- Chave estrangeira: Vincula a alteração ao usuário responsável.
    cpf VARCHAR(14) NOT NULL,
    FOREIGN KEY (cpf) REFERENCES usuario (cpf)
);

-- ---------------------------------------------------------------------------------------------------------
-- 5. TABELA CARACTERISTICA
-- Propósito: Definir atributos configuráveis para os produtos (ex: "Cor", "Material", "Voltagem").
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS caracteristica (
    -- Chave primária: Identificador único da característica.
    cod_caracteristica INT PRIMARY KEY AUTO_INCREMENT,
    -- Nome da característica (e.g., 'Cor', 'Tamanho').
    nome VARCHAR(100),
     -- Data e hora que a caracteristica foi cadastrada.
    data_hora DATETIME NOT NULL,
    -- Chave estrangeira: Vincula a característica a um tipo de produto específico.
    cod_tipo INT,
    -- Chave estrangeira: Vincula a criação/gestão da característica ao usuário.
    cpf VARCHAR(14) NOT NULL, 
    FOREIGN KEY (cpf) REFERENCES usuario (cpf),
    FOREIGN KEY (cod_tipo) REFERENCES tipo (cod_tipo)
);

-- ---------------------------------------------------------------------------------------------------------
-- 6. TABELA ESTANTE
-- Propósito: Mapear o endereçamento físico do estoque.
-- INTEGRAÇÃO: Inclui vínculo com a categoria para demarcar o que pode ser armazenado.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS estante (
	-- Chave primária: Identificador único da estante 
	cod_estante INT PRIMARY KEY auto_increment,
    -- Identificador da estante.
    nome VARCHAR(10),
     -- Data e hora que a estante foi cadastrada.
    data_hora DATETIME NOT NULL,
    -- Chave estrangeira: Usuário responsável pela gestão ou criação da estante.
    cpf VARCHAR(14) NOT NULL,
    -- Chave estrangeira: Define a categoria de produtos permitida nesta estante.
    cod_categoria INT, 
    FOREIGN KEY (cpf) REFERENCES usuario (cpf),
    FOREIGN KEY (cod_categoria) REFERENCES categoria (cod_categoria)
);

-- ---------------------------------------------------------------------------------------------------------
-- 7. TABELA PEDIDO
-- Propósito: Registrar as transações de pedidos realizadas no sistema.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido (
    -- Chave primária: Identificador único do pedido.
    cod_pedido INT PRIMARY KEY AUTO_INCREMENT,
    -- Chave estrangeira: Usuário que realizou o pedido.
    cpf VARCHAR(14) NOT NULL,
    -- Data e hora exata em que o pedido foi registrado.
    data_pedido DATETIME,
    FOREIGN KEY (cpf) REFERENCES usuario (cpf)
);

-- ---------------------------------------------------------------------------------------------------------
-- 8. TABELA PRODUTO
-- Propósito: Catálogo de produtos.
-- INTEGRAÇÃO: Vinculado a 'tipo' para herdar características específicas.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS produto (
    -- Chave primária: Identificador único do produto.
    cod_produto INT PRIMARY KEY AUTO_INCREMENT,
    -- Chave estrangeira: Usuário responsável pela criação/cadastro do produto.
    cpf VARCHAR(14) NOT NULL,
    -- Stock Keeping Unit (código de identificação interna do produto).
    sku VARCHAR(100),
    -- Imagem do produto, armazenada como BLOB (Binary Large Object).
    imagem BLOB,
    -- Descrição longa do produto.
    descricao VARCHAR(255),
    -- Nome comercial do produto.
    nome VARCHAR(100),
    -- Valor unitário do produto.
    valor FLOAT(10),
    -- Data e hora que o produto foi cadastrado.
    data_hora DATETIME NOT NULL,
    -- Chave estrangeira: Vincula o produto ao seu tipo específico.
	cod_estante INT, 
    cod_tipo INT, 
    FOREIGN KEY (cpf) REFERENCES usuario (cpf),
    FOREIGN KEY (cod_estante) REFERENCES estante (cod_estante),
    FOREIGN KEY (cod_tipo) REFERENCES tipo (cod_tipo)
);

-- ---------------------------------------------------------------------------------------------------------
-- 9. TABELA PRODUTO_CARACTERISTICA
-- Propósito: Tabela de junção para a relação M:N (Produto x Característica), armazenando o valor da característica.
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS produto_caracteristica (
    -- Chave primária: Identificador único da relação Produto-Característica.
    cod_prod_caracteristica INT PRIMARY KEY AUTO_INCREMENT,
    -- Valor específico da característica para aquele produto (ex: 'Vermelho' para a Característica 'Cor').
    valor VARCHAR(255),
    -- Chave estrangeira: Produto envolvido.
    cod_produto INT,
    -- Chave estrangeira: Característica referenciada.
    cod_caracteristica INT,
    FOREIGN KEY (cod_produto) REFERENCES produto (cod_produto),
    FOREIGN KEY (cod_caracteristica) REFERENCES caracteristica (cod_caracteristica)
);

-- ---------------------------------------------------------------------------------------------------------
-- 10. TABELA ARMAZENAMENTO
-- Propósito: Rastrear a quantidade de um produto em uma estante específica (controle de estoque por localização).
-- É uma tabela de junção com chave primária composta (PK composta).
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS armazenamento (
    -- Colunas da chave primária composta (identificador de armazém/posição).
    cod_armazem INT NOT NULL,
    cod_produto INT NOT NULL,
    cod_estante INT NOT NULL,
    -- Quantidade do produto no local especificado.
    quantidade INT,
    PRIMARY KEY (cod_armazem, cod_produto, cod_estante),
    -- Chave estrangeira: Produto em estoque.
    FOREIGN KEY (cod_produto) REFERENCES produto (cod_produto),
    -- Chave estrangeira: Localização (endereçamento) na estante.
    FOREIGN KEY (cod_estante) REFERENCES estante (cod_estante)
);

-- ---------------------------------------------------------------------------------------------------------
-- 11. TABELA ITEM_PEDIDO
-- Propósito: Detalhar os produtos e quantidades de cada pedido (relação M:N entre Pedido e Produto).
-- ---------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS item_pedido (
    -- Colunas da chave primária composta (garante unicidade para cada item dentro de um pedido).
    cod_pedido INT NOT NULL,
    cod_produto INT NOT NULL,
    -- Quantidade do produto neste item do pedido.
    quantidade INT,
    PRIMARY KEY (cod_pedido, cod_produto),
    -- Chave estrangeira: Pedido ao qual o item pertence.
    FOREIGN KEY (cod_pedido) REFERENCES pedido (cod_pedido),
    -- Chave estrangeira: Produto que está sendo pedido.
    FOREIGN KEY (cod_produto) REFERENCES produto (cod_produto)
);
