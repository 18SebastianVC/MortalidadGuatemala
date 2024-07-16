CREATE PROCEDURE InsertarCausaMuerte
    @causa varchar(250)
AS
BEGIN
    -- Verificar si la causa de muerte ya existe en la tabla
    IF NOT EXISTS (SELECT 1 FROM CausasMuerte WHERE causa = @causa)
    BEGIN
        -- Insertar la nueva causa de muerte
        INSERT INTO CausasMuerte (causa)
        VALUES (@causa)
    END
END

CREATE PROCEDURE InsertarFecha
    @fecha AS VARCHAR(10)
AS
BEGIN
    -- Convertir la fecha al formato "yyyy-mm-dd" para comparación
    DECLARE @fechaConvertida AS DATE = CONVERT(DATE, @fecha, 103)

    -- Verificar si la fecha ya existe en la tabla
    IF NOT EXISTS (SELECT 1 FROM Tiempo WHERE FechaDefuncion = @fechaConvertida)
    BEGIN
        -- Insertar la fecha en la tabla
        INSERT INTO Tiempo (FechaDefuncion) VALUES (@fechaConvertida)
    END
END

CREATE PROCEDURE InsertarDepartamento
    @departamento VARCHAR(16)
AS
BEGIN
    -- Verificar si el departamento ya existe en la tabla
    IF NOT EXISTS (SELECT 1 FROM Ubicacion WHERE Departamento = @departamento)
    BEGIN
        -- Insertar el departamento en la tabla
        INSERT INTO Ubicacion (Departamento) VALUES (@departamento)
    END
END