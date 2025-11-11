# Electiva1

import psycopg2
from psycopg2 import sql
import credentials
import sys
import csv

def delete_line():
    sys.stdout.write("\r")  # Move the cursor back to the beginning of the line
    sys.stdout.write(" " * 50)  # Overwrite the line with spaces (adjust the number based on the length of your line)
    sys.stdout.write("\r")  # Move the cursor back to the beginning again
    sys.stdout.flush()

def create_table(cursor,table):
    try:
        # Verificar si la tabla ya existe
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '"+ table + "');")
        table_exists = cursor.fetchone()[0]

        # Crear la tabla solo si no existe
        if not table_exists:
            cursor.execute("CREATE TABLE {s_table} (registro serial PRIMARY KEY, frame INTEGER, articulacion VARCHAR(50), cord_x FLOAT, cord_y FLOAT, cord_z FLOAT);".format(s_table=table))
            
            print("Finished creating table")
        else:
            print("Table '"+ table +"' already exists.")
    except Exception as e:
        print("Error creating table:", str(e))
        raise

   
def insert(cursor,table,info):
  try: 
    cursor.execute("INSERT INTO " + table +" (frame, articulacion, cord_x, cord_y, cord_z) VALUES (%s, %s, %s, %s, %s);", (info[0], info[1] ,info[2],info[3],info[4]))
  except:
    raise

def insert_from_csv(cursor, table, csv_file_path):
    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file) 
            # next(reader)  # Saltar la primera fila si contiene encabezados
            
            i = 0
            for row in reader:
                # Insertar cada fila en la base de datos
                print(row)
                #row_v = row.split(",")
                insert(cursor, table, row)
                
                print("Lineas subidas a la bd: "+str(i), end="", flush=True)
                delete_line()
                i+=1           
                if i > 5: 
                   break     
        print("Data inserted from CSV successfully.")
    except Exception as e:
        print("Error inserting data from CSV:", str(e))
        raise
  
def update(cursor):
  try:
    cursor.execute("UPDATE inventory SET quantity = %s WHERE name = %s;", (200, "banano"))
    print("Updated 1 row of data")
  except:
    raise

def delete(cursor):
  try:
    cursor.execute("DELETE FROM inventory WHERE name = %s;", ("naranja",))
    print("Deleted 1 row of data")
  except:
    raise

def delete_table(table_name, cursor):
    try:
        # Obtener identificador de la tabla
        table_identifier = sql.Identifier(table_name)

        # Solicitud SQL a ejecutar
        query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(table_identifier)

        # Ejecuta instrucción
        cursor.execute(query)

        print(f"Tabla '{table_name}' eliminada exitosamente.")

    except psycopg2.Error as e:
        print(f"Error eliminando table '{table_name}': {e}")
  
def read(cursor,table):
  try:
    # Fetch all rows from table
    cursor.execute("SELECT * FROM " + table + ";")
    rows = cursor.fetchall()

    # Print all rows
    for row in rows:
        print("Data row(",end="")
        for i, item in enumerate(row):
          print(item, end=", " if i < len(row) - 1 else ")\n")
        
        
  except:
    raise

def get_table_names(cursor):
    try:
        # Ejecutar la consulta SQL para obtener los nombres de las tablas
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        
        # Obtener todos los nombres de las tablas
        table_names = [row[0] for row in cursor.fetchall()]
        
        return table_names
    except Exception as e:
        print("Error al obtener nombres de tablas:", str(e))
        raise