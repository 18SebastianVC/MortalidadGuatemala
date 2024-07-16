CREATE DATABASE usac;

USE usac;

CREATE TABLE Personas(
	Id INT PRIMARY KEY,
	Edad SMALLINT,
	Genero VARCHAR(12),
);

CREATE TABLE CausasMuerte(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Causa VARCHAR(250) UNIQUE,
);

CREATE TABLE Ubicacion(
	Id SMALLINT PRIMARY KEY IDENTITY(1,1),
	Departamento VARCHAR(16),
);

CREATE TABLE Tiempo(
	Id INT PRIMARY KEY IDENTITY(1,1),
	FechaDefuncion DATE,
);

CREATE TABLE Defunciones(
	Id INT PRIMARY KEY IDENTITY(1,1),
	IdTiempo INT,
	IdUbicacion SMALLINT,
	IdPersona INT,
	IdCausa INT
);

ALTER TABLE Defunciones 
ADD CONSTRAINT fk_defuncion_persona 
FOREIGN KEY (IdPersona)
REFERENCES Personas (Id);

ALTER TABLE Defunciones 
ADD CONSTRAINT fk_defuncion_causa 
FOREIGN KEY (IdCausa)
REFERENCES CausasMuerte (Id);

ALTER TABLE Defunciones 
ADD CONSTRAINT fk_defuncion_tiempo 
FOREIGN KEY (IdTiempo)
REFERENCES Tiempo (Id);

ALTER TABLE Defunciones 
ADD CONSTRAINT fk_defuncion_ubicacion 
FOREIGN KEY (IdUbicacion)
REFERENCES Ubicacion (Id);