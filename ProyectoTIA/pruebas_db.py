# factores_multiplicadores = (2.4, 2.0, 0.0)
# ruta_txt = "C:/Users/user/OneDrive - Universidad Nacional de Colombia/Semestre 92/TIA/ProyectoTIA/Datos_video.txt"

# with open(ruta_txt, 'r') as file:
#     lineas = file.readlines()
#     articulaciones = []
#     for line in lineas:
#         articulacion = line.split(sep=',')[1]
#         if not(articulacion in articulaciones):
#             articulaciones.append(articulacion)
#     num_objetos = len(articulaciones)

# # Crear objetos en la posición inicial
# for i in range(num_objetos):
#     # Obtener las coordenadas multiplicadas por los factores correspondientes
#     print(lineas[i % num_objetos].split(',')[2:5])
#     coordenadas_iniciales = [float(coord) * factores_multiplicadores[j % 3] for j, coord in enumerate(lineas[i % num_objetos].split(',')[2:5])]
#     print(coordenadas_iniciales)
# # print(lineas)

# #print(lineas)  
from data_base import *

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(credentials.host, credentials.user, credentials.dbname, credentials.password, credentials.sslmode)
conn = psycopg2.connect(conn_string) 
print("Connection established")
cursor = conn.cursor()

table_names = get_table_names(cursor)
print("Nombres de las tablas en la base de datos:")
for table_name in table_names:
    print(table_name)
table_selected = input("Ingrese el caso que desea eliminar: ")
delete_table(table_selected, cursor)
conn.commit()
