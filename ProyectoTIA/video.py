import cv2
import mediapipe as mp #version 3.8.10 de python o marca error
import csv
from data_base import *

# Funciones

def articulaciones(digito):
    if digito == 0:
        return "NOSE"
    elif digito == 1:
        return "LEFT_EYE_INNER"
    elif digito == 2:
        return "LEFT_EYE"
    elif digito == 3:
        return "LEFT_EYE_OUTER"
    elif digito == 4:
        return "RIGHT_EYE_INNER"
    elif digito == 5:
        return "RIGHT_EYE"
    elif digito == 6:
        return "RIGHT_EYE_OUTER"
    elif digito == 7:
        return "LEFT_EAR"
    elif digito == 8:
        return "RIGHT_EAR"
    elif digito == 9:
        return "MOUTH_LEFT"
    elif digito == 10:
        return "MOUTH_RIGHT"
    elif digito == 11:
        return "LEFT_SHOULDER"
    elif digito == 12:
        return "RIGHT_SHOULDER"
    elif digito == 13:
        return "LEFT_ELBOW"
    elif digito == 14:
        return "RIGHT_ELBOW"
    elif digito == 15:
        return "LEFT_WRIST"
    elif digito == 16:
        return "RIGHT_WRIST"
    elif digito == 17:
        return "LEFT_PINKY"
    elif digito == 18:
        return "RIGHT_PINKY"
    elif digito == 19:
        return "LEFT_INDEX"
    elif digito == 20:
        return "RIGHT_INDEX"
    elif digito == 21:
        return "LEFT_THUMB"
    elif digito == 22:
        return "RIGHT_THUMB"
    elif digito == 23:
        return "LEFT_HIP"
    elif digito == 24:
        return "RIGHT_HIP"
    elif digito == 25:
        return "LEFT_KNEE"
    elif digito == 26:
        return "RIGHT_KNEE"
    elif digito == 27:
        return "LEFT_ANKLE"
    elif digito == 28:
        return "RIGHT_ANKLE"
    elif digito == 29:
        return "LEFT_HEEL"
    elif digito == 30:
        return "RIGHT_HEEL"
    elif digito == 31:
        return "LEFT_FOOT_INDEX"
    elif digito == 32:
        return "RIGHT_FOOT_INDEX"
    else:
        return "DÍGITO_NO_VÁLIDO"

def analyse_video():
    # Código de mediapy
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture("salsa.mp4")

    with mp_pose.Pose(static_image_mode=False) as pose:
        with open("Datos_video.txt", "w", newline='') as txt_file: # "a" para continuar escribiendo en el archivo; "w" para dejar enblaoc y escribir
            txt_writer = csv.writer(txt_file)

            n=0 
            while True:
                ret, frame = cap.read()
                if not ret:
                    break   


                height, width, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                
                # Convierte los landmarks en una cadena de texto y escribe en el archivo
                if results.pose_landmarks is not None:
                    landmarks_data = []
                    punto = 0
                    for landmark in results.pose_landmarks.landmark:
                        points_deleted = list(range(1,9))
                        if not (punto in points_deleted):
                            txt_file.write(f"{n},{articulaciones(punto)},{landmark.x},{landmark.z},{landmark.y}\n")
                        # landmarks_data.append(n)
                        # landmarks_data.append(articulac2iones(punto))
                        # landmarks_data.append(landmark.x)
                        # landmarks_data.append(landmark.y)
                        # landmarks_data.append(landmark.z)
                        # csv_writer.writerow(landmarks_data)
                        # landmarks_data =[]
                        punto+=1

    #esto es para visualizar el seguimiento de los puntos en el video
            
                if results.pose_landmarks is not None:
                    mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(128, 0,250), thickness = 2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=( 255, 255,255), thickness = 2)
                )
            
                n+=1

                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

    cap.release()
    cv2.destroyAllWindows()



# Inicialización de la base de datos
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(credentials.host, credentials.user, credentials.dbname, credentials.password, credentials.sslmode)
conn = psycopg2.connect(conn_string) 
print("Connection established")
cursor = conn.cursor()

# Menú de navegación 
while True:
    
    print("""
      Bienvenido. Usted desea:  
      1. Consultar un caso ya analizado.\n
      2. Analizar un video nuevo.\n
      3. Borrar caso existente. \n 
      4. Cerrar connecion.\n
      5. Salir.
      """
    )  
    option = int(input("Ingrese una opcion: "))
    match option:
      
    
      case 1:
        table_names = get_table_names(cursor)
        print("Nombres de las tablas en la base de datos:")
        for table_name in table_names:
            print(table_name)
        table_selected = input("Ingrese el caso que desea consultar: ")
        read(cursor,table_selected)
      
      case 2:
        while True:
            save_in_db_str = input("¿Desea guardar la información en la base de datos? (S/N): ")
            if save_in_db_str == "S" or save_in_db_str == "N":
                break

        if(save_in_db_str == "S"):
            save_in_db = True
            table_name = input("Ingrese el nombre de la prueba: ")
            create_table(cursor,table_name)
        else: 
            save_in_db = False

        analyse_video()
        if(save_in_db):
            insert_from_csv(cursor, table_name, "Datos_video.txt")
      
      case 3: 
            table_names = get_table_names(cursor)
            print("Nombres de las tablas en la base de datos:")
            for table_name in table_names:
                print(table_name)
            table_selected = input("Ingrese el caso que desea eliminar: ")
            delete_table(table_selected, cursor)
        
      case 4:
        confirmation = input("¿Seguro de cerrar la conexión? (S/N)")
        if(confirmation=="S"):
          conn.commit()
          cursor.close()
          conn.close()
        
      case 5:
        sys.exit()
        
      case _:
        print('Opcion incorrecta')
    
    conn.commit()