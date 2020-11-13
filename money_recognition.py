import io
import os
from picamera import PiCamera
from google.cloud import vision
from google.cloud.vision import types
from gtts import gTTS
from PIL import Image, ImageFilter
from enum import Enum

try:
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="apikey.json"


	os.system("mpg321 audios_definidos/inicio_billetes.mp3")
	val_word = ['Banknote','Money','Cash','Banco']

	veinte = 'Veinte Pesos'
	cincuenta = 'Cincuenta Pesos'
	cien = 'Cien Pesos'
	doscientos = 'Doscientos Pesos'
	quinientos = 'Quinientos Pesos'
	mil = 'Mil Pesos'

	veinte_n = '20'
	cincuenta_n = '50'
	cien_n = '100'
	doscientos_n = '200'
	quinientos_n = '500'
	mil_n = '1000'

	def count_word(cad):
		cont = 0
		for word in val_word:
			if word in cad:
				cont = cont + 1
		return cont > 1
			


	# Instantiates a clien
	camera = PiCamera()
	camera.start_preview()
	camera.capture('fotos_billetes/billete.png', format='png', resize=(840,480))
	camera.close()
	
	client = vision.ImageAnnotatorClient()
	# The name of the image file to annotate
	file_name = os.path.join(
	    os.path.dirname(__file__),
	    'fotos_billetes/billete.png')
	    
	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations
	print('------Labels:------')
	label_acum = ""
	for label in labels:
		label_acum = label_acum + label.description + " "
		
	print(label_acum)

	response = client.document_text_detection(image=image)
	texts = response.text_annotations
	text_acum = ""
	print('------Texts:------')
	for text in texts:
		text_acum += text.description + " "
		
	print(text_acum)

				
	response = client.web_detection(image=image)
	annotations = response.web_detection
	web_acum = ""
	print('------Webs:------')
	if annotations.best_guess_labels:
		for label in annotations.best_guess_labels:
			web_acum += label.label + " "
			
	print(web_acum)
	text_acum = text_acum + " " + web_acum

	if count_word(label_acum):
		if mil in text_acum or mil_n in text_acum:
			os.system("mpg321 audios_definidos/billete_mil.mp3")
		elif quinientos in text_acum or quinientos_n in text_acum:
			os.system("mpg321 audios_definidos/billete_quinientos.mp3")
		elif doscientos in text_acum or doscientos_n in text_acum:
			os.system("mpg321 audios_definidos/billete_doscientos.mp3")
		elif cien in text_acum or cien_n in text_acum:
			os.system("mpg321 audios_definidos/billete_cien.mp3")
		elif cincuenta in text_acum or cincuenta_n in text_acum:
			os.system("mpg321 audios_definidos/billete_cincuenta.mp3")
		elif veinte in text_acum or veinte_n in text_acum:
			os.system("mpg321 audios_definidos/billete_veinte.mp3")
		else:
			os.system("mpg321 audios_definidos/error_billetes.mp3")
	else:
		os.system("mpg321 audios_definidos/error_billetes.mp3")

except Exception as e:
    print(e)
    os.system("mpg321 audios_definidos/algo_mal.mp3")

