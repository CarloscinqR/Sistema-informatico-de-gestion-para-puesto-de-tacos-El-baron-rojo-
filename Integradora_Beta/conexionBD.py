import mysql.connector

def reconectar():
    """Reconecta automáticamente si la conexión murió."""
    global conexion, cursor
    try:
        # intenta reconectar, y si está caída la levanta
        conexion.ping(reconnect=True, attempts=3, delay=2)

        # si el cursor ya no existe o fue cerrado → se crea uno nuevo
        if cursor is None or cursor.closed:
            cursor = conexion.cursor(buffered=True)

    except:
        # la conexión murió por completo → crear una nueva
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='bd_baron_rojo'
            )
            cursor = conexion.cursor(buffered=True)
        except Exception as e:
            print("ERROR reconectando a la BD:", e)


# ----------- Conexión inicial -------------
try:
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='bd_baron_rojo'
    )
    cursor = conexion.cursor(buffered=True)
except Exception as e:
    print("Ocurrió un error con el Sistema:", e)
