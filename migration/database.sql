-- criando e usando o banco de dados chamado 'tcc_logistica'
CREATE DATABASE IF NOT EXISTS tcc_logistica;
use tcc_logistica;



-- Tabela para armazenar as categorias de produtos.
CREATE TABLE IF NOT EXISTS categoria (

    cod_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100)
    
);



-- Tabela para os tipos de produtos, vinculada à categoria.
CREATE TABLE IF NOT EXISTS tipo (

    cod_tipo INT PRIMARY KEY AUTO_INCREMENT,
    nome CHAR(10),
    cod_categoria INT,
    FOREIGN KEY (cod_categoria) REFERENCES categoria (cod_categoria)

);



-- Tabela de usuários, identificados pelo CPF.
CREATE TABLE IF NOT EXISTS usuario (

    cpf VARCHAR(11) PRIMARY KEY NOT NULL,
    nome VARCHAR(100),
    senha VARCHAR(255)

);



-- Tabela para registrar alterações em produtos e estantes, vinculada ao usuário que a realizou.
CREATE TABLE IF NOT EXISTS alteracao_produto_estante (

    cod_alteracao INT PRIMARY KEY AUTO_INCREMENT,
    alteracao_realizada VARCHAR(255),
    cpf VARCHAR(11) NOT NULL,
    FOREIGN KEY (cpf) REFERENCES usuario (cpf)

);



-- Tabela para armazenar características de produtos, vinculada ao tipo de produto.
CREATE TABLE IF NOT EXISTS caracteristica (

    cod_caracteristica INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    cod_tipo INT,
    cpf VARCHAR(11) NOT NULL,
    FOREIGN KEY (cpf) REFERENCES usuario (cpf),
    FOREIGN KEY (cod_tipo) REFERENCES tipo (cod_tipo)

);



-- Tabela para gerenciar as estantes no estoque, vinculada ao usuário.
CREATE TABLE IF NOT EXISTS estante (

    enderecamento INT PRIMARY KEY NOT NULL,
    estante VARCHAR(10),
    linha VARCHAR(10),
    coluna VARCHAR(10),
    cpf VARCHAR(11) NOT NULL,
    FOREIGN KEY (cpf) REFERENCES usuario (cpf)

);



-- Tabela de pedidos, vinculada ao usuário que o realizou.
CREATE TABLE IF NOT EXISTS pedido (

    cod_pedido INT PRIMARY KEY AUTO_INCREMENT,
    cpf VARCHAR(11) NOT NULL,
    data_pedido DATETIME,
    FOREIGN KEY (cpf) REFERENCES usuario (cpf)

);



-- Tabela para os produtos.
CREATE TABLE IF NOT EXISTS produto (

    cod_produto INT PRIMARY KEY AUTO_INCREMENT,
    cpf VARCHAR(11) NOT NULL,
    categoria VARCHAR(100),
    sku VARCHAR(100),
    imagem BLOB,
    descricao VARCHAR(255),
    nome VARCHAR(100),
    valor FLOAT(10),
    FOREIGN KEY (cpf) REFERENCES usuario (cpf)

);



-- Tabela para vincular produtos a suas características.
-- Observe que o campo 'cod_caracteristica' é agora do tipo INT para corresponder à tabela 'caracteristica'.
CREATE TABLE IF NOT EXISTS produto_caracteristica (

    cod_prod_caracteristica INT PRIMARY KEY AUTO_INCREMENT,
    valor DECIMAL(10, 2),
    cod_produto INT,
    cod_caracteristica INT,
    FOREIGN KEY (cod_produto) REFERENCES produto (cod_produto),
    FOREIGN KEY (cod_caracteristica) REFERENCES caracteristica (cod_caracteristica)

);



-- Tabela para gerenciar o armazenamento de produtos nas estantes.
CREATE TABLE IF NOT EXISTS armazenamento (

    cod_armazem INT NOT NULL,
    cod_produto INT NOT NULL,
    enderecamento INT NOT NULL,
    quantidade INT,
    PRIMARY KEY (cod_armazem, cod_produto, enderecamento),
    FOREIGN KEY (cod_produto) REFERENCES produto (cod_produto),
    FOREIGN KEY (enderecamento) REFERENCES estante (enderecamento)

);



-- Tabela para detalhar os itens de um pedido.
CREATE TABLE IF NOT EXISTS item_pedido (

    cod_pedido INT NOT NULL,
    cod_produto INT NOT NULL,
    quantidade INT,
    PRIMARY KEY (cod_pedido, cod_produto),
    FOREIGN KEY (cod_pedido) REFERENCES pedido (cod_pedido),
    FOREIGN KEY (cod_produto) REFERENCES produto (cod_produto)

);