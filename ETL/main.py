import os
import re
import pandas as pd
import pyodbc

# Configuración de la conexión a la base de datos
# Se deben ingresar las credenciales correspondientes
server = ''
database = ''
username = ''
password = ''

# Cadena de conexión
conn_str = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

#Iniciar conexion
print('Iniciando conexion')
try:
    conn = pyodbc.connect(conn_str,autocommit=True)
except:
    # Código que se ejecutará si se produce una excepción
    print("Se produjo una excepción")
    exit()

print('Conexion exitosa')

#Variables globales
patron = re.compile("[a-zA-Z]")
ruta_csv=''
dataFrame=None

def Transformar(df_):
    i = 0 # Este indice sirve unicamente para verificar el avance de la carga de datos. No afecta en el funcionamiento
    for row in df_.itertuples():
        i = i +1
        if i % 1000 == 0:
            print(">",i,": ",row[2])
        
        IdPersona=GetIdPersona(row[1],row[4],row[5])
        IdFecha=GetIdFecha(row[3])
        IdDepartamento=GetIdDepartamento(row[6])

        for indice in range(7, 11):
            if isinstance(row[indice], str): #Verificar si es string o espacio vacio
                if patron.search(row[indice]): # Verificar si tiene letras
                    IdCausa=GetIdCausa(row[indice]) 
                    RegistrarDefuncion(IdFecha,IdDepartamento,IdPersona,IdCausa)
        # print(">",i,": ",row[1],", ",row[2])
    print('Finalizada la carga de datos')

def GetIdPersona(item1,item2,item3):
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO Personas (Id,Edad,Genero) VALUES ({item1},\'{item2}\',\'{item3}\')')
    return item1

def GetIdFecha(item):
    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()
    
    # Definir los parámetros de entrada y salida del procedimiento almacenado
    fecha = item
    fechaId=None

    # Ejecutar el procedimiento almacenado
    cursor.execute("{CALL InsertarFecha(?)}", fecha)

    # Ejecutar la consulta para buscar el ID de la fecha
    cursor.execute("SELECT Id FROM Tiempo WHERE FechaDefuncion = CONVERT(DATE, ?, 103)", fecha)

    # Obtener el resultado de la consulta
    row = cursor.fetchone()
    if row:
        # Imprimir el ID de la fecha encontrada
        fechaId = row[0]
    else:
        fechaId = 1
        print("No se encontró ninguna fecha con ese nombre.")
    cursor.close()
    return fechaId

def GetIdDepartamento(item):
    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()
    
    # Definir los parámetros de entrada y salida del procedimiento almacenado
    Departamento = item
    DepartamentoId=None

    # Ejecutar el procedimiento almacenado
    cursor.execute("{CALL InsertarDepartamento(?)}", Departamento)

    # Ejecutar la consulta para buscar el ID de la Departamento
    cursor.execute("SELECT Id FROM Ubicacion WHERE Departamento = ?", Departamento)

    # Obtener el resultado de la consulta
    row = cursor.fetchone()
    if row:
        # Imprimir el ID de la Departamento encontrada
        DepartamentoId = row[0]
    else:
        DepartamentoId = 1
        print("No se encontró ninguna Departamento con ese nombre.")
    cursor.close()
    return DepartamentoId

def GetIdCausa(item):
    item=Limpieza(item)
    
    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()
    
    # Definir los parámetros de entrada y salida del procedimiento almacenado
    causa = item
    causaId=None

    # Ejecutar el procedimiento almacenado
    cursor.execute("{CALL InsertarCausaMuerte(?)}", causa)

    # Ejecutar la consulta para buscar el ID de la causa
    cursor.execute("SELECT ID FROM CausasMuerte WHERE causa = ?", causa)

    # Obtener el resultado de la consulta
    row = cursor.fetchone()

    if row:
        # Imprimir el ID de la causa encontrada
        causaId = row[0]
    else:
        causaId = 1
        print("No se encontró ninguna causa con ese nombre.")

    cursor.close()
    return causaId

def Limpieza(cadena):
    # Convertir a minusculas para que sea mas sencillo hacer la limpieza
    cadena = cadena.lower()

    # Eliminar tildes
    cadena = cadena.replace("'", "''")
    cadena = cadena.replace("á", "a")
    cadena = cadena.replace("é", "e")
    cadena = cadena.replace("í", "i")
    cadena = cadena.replace("ó", "o")
    cadena = cadena.replace("ú", "u")

    # Espacios dobles
    cadena = cadena.replace("  ", " ")

    # Caracteres sobrantes al final
    cadena = cadena.rstrip(".")
    cadena = cadena.rstrip(",")
    cadena = cadena.rstrip("-")
    cadena = cadena.rstrip() #Espacio en blanco

    # Patrón para eliminar o reemplazar abreviaturas al inicio de la cadena
    cadena = re.sub(r'^a\) ', '', cadena)
    cadena = re.sub(r'^a\.\) ', '', cadena)
    cadena = re.sub(r'^a\. ', '', cadena)
    cadena = re.sub(r'^c\.a\. ', 'carcinoma ', cadena)
    cadena = re.sub(r'^c\.a ', 'carcinoma ', cadena)
    cadena = re.sub(r'^ca\. ', 'carcinoma ', cadena)
    cadena = re.sub(r'^ca ', 'carcinoma', cadena)

    #Errores comunes. Los tipos se escriben ese orden para que no se altere el replace
    

    # Retornar la cadena de texto en formato Capitalizado
    cadena = cadena.capitalize()
    
    return cadena

def RegistrarDefuncion(fecha_,departamento_,idpersona_,idcausa_):
    cursor = conn.cursor()
    sql = "INSERT INTO Defunciones (IdTiempo, IdUbicacion, IdPersona, IdCausa) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, fecha_, departamento_, idpersona_, idcausa_)
    return 1

# Se debe cargar el archivo csv con la data
dataFrame= pd.read_csv('data.csv')
Transformar(dataFrame)
conn.close()
exit()

