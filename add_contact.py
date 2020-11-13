#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import os
import speech_recognition as sr
from picamera import PiCamera
import re
from unicodedata import normalize
import RPi.GPIO as GPIO
import time

# Record Audio
r = sr.Recognizer()
language_opt = "es-ES"
os.system("mpg321 audios_definidos/nombre_contacto.mp3")

with sr.Microphone() as source:
  #r.energy_threshold = 400
  r.adjust_for_ambient_noise(source)
  audio = r.listen(source)
  try:
      escucha = r.recognize_google(audio, language=language_opt).lower()
      print(escucha)
      camera = PiCamera()
      escucha = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",normalize( "NFD", escucha), 0, re.I)
      escucha = normalize( 'NFC', escucha)
      print( escucha )
      
      camera.capture('fotos_rostros/'+escucha+'.png', format='png', resize=(840,480))
      camera.close()
      f = open("fotos_rostros/nombres.txt", "a")
      f.write("\n" + escucha)
      f.close()
      os.system("mpg321 audios_definidos/contacto_agregado.mp3")
      #break
  except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
      os.system("mpg321 audios_definidos/no_entendi.mp3")
  except sr.RequestError as e:
      os.system("mpg321 audios_definidos/error_internet.mp3")
      print("Could not request results from Google Speech Recognition service; {0}".format(e))
  except Exception as e:
      print(e)
      os.system("mpg321 audios_definidos/algo_mal.mp3")
