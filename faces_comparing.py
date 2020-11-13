import face_recognition
from picamera import PiCamera
from PIL import Image, ImageDraw
import numpy as np
from gtts import gTTS
import os
import time
try:
    os.system("mpg321 audios_definidos/inicio_faces.mp3")

    f = open("fotos_rostros/nombres.txt", "r")
    known_face_names = f.read().split("\n")
    print(known_face_names)

    known_face_encodings = []

    for name in known_face_names:
        face_image = face_recognition.load_image_file("fotos_rostros/"+name+".png")
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_face_encodings.append(face_encoding)


    camera = PiCamera()
    camera.start_preview()
    camera.capture('fotos_rostros/ejemplo.png', format='png', resize=(840,480))
    camera.close()
        
    unknown_image = face_recognition.load_image_file("fotos_rostros/ejemplo.png")

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)


    conocidos=""
    desconocidos = 0
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconocido "
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            conocidos+=name+", "
        else:
            desconocidos=desconocidos+1


    desc=str(desconocidos)
    texto="Detecté a "+conocidos+" y un total de "+desc+" desconocidos"
    print("\n\n" + texto + "\n\n" )
    tts = gTTS(text=texto,lang='es')
    tts.save("audios_generados/faces_comparing.mp3")
    os.system("mpg321 audios_generados/faces_comparing.mp3")
except Exception as e:
    print("Error de internet: {0}".format(e))
    os.system("mpg321 audios_definidos/algo_mal.mp3")

