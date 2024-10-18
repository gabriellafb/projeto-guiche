
CREATE TABLE cliente(
	id_cliente int not null PRIMARY KEY AUTO_INCREMENT
	nome_cliente varchar(50)
	sobrenome_cliente varchar(50)
	email_cliente varchar(255)
	
);


CREATE TABLE servicos (
    id_servico INT PRIMARY KEY AUTO_INCREMENT,
    nome_servico VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    preço DECIMAL(10, 2) NOT NULL,
    duração_estimativa INT,
    disponibilidade BOOLEAN DEFAULT TRUE
);