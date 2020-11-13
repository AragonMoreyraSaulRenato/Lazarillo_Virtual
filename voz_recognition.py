#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import os
import speech_recognition as sr

# Record Audio
r = sr.Recognizer()
key_word = "coco"
text_word = "lee"
face_word = "personas"
money_word = "dinero"
cancel_word = "cancelar"
add_contact ="agregar"
language_opt = "es-ES"

while True:
    try:
        with sr.Microphone() as source:
            r.dynamic_energy_threshold = False
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            escucha = r.recognize_google(audio, language=language_opt).lower()
            print(escucha)
            
            if text_word in escucha:
                print("Lectura")
                os.system("python text_recognition.py")
            elif face_word in escucha:
                print("Rostros")
                os.system("python3 faces_comparing.py")
            elif add_contact in escucha:
                print("Agregar Contacto")
                os.system("python3 add_contact.py")
            elif money_word in escucha:
                print("Billetes")
                os.system("python money_recognition.py")
            else:
                print("No reconozco comando")
                os.system("mpg321 audios_definidos/error_comando.mp3")
                
           
    except sr.UnknownValueError:
        print("No entendio el audio")
        os.system("mpg321 audios_definidos/no_entendi.mp3")
    except sr.RequestError as e:
        print("Error de internet: {0}".format(e))
        os.system("mpg321 audios_definidos/error_internet.mp3")
