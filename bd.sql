CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(id),
    servico_id INT REFERENCES servicos(id),
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'Pendente'
);
