
CREATE TABLE usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    senha VARCHAR(255)
	
);


CREATE TABLE servicos (
    id_servico INT PRIMARY KEY AUTO_INCREMENT,
    nome_servico VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    preço DECIMAL(10, 2) NOT NULL,
    duração_estimativa INT,
    disponibilidade BOOLEAN DEFAULT TRUE
);