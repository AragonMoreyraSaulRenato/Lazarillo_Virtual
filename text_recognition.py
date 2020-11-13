import io
import os
from picamera import PiCamera
from google.cloud import vision
from google.cloud.vision import types
from gtts import gTTS
from PIL import Image, ImageFilter
try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="apikey.json"
    os.system("mpg321 audios_definidos/inicio_texto.mp3")

    #TOMANDO FOTO
    camera = PiCamera()
    camera.start_preview()
    camera.capture('fotos_textos/text.png', format='png', resize=(840,480))
    camera.close()


    path = 'fotos_textos/text.png'


    #NITIDEZ
    foto = Image.open(path).convert('L')
    #Laplace
    coeficientes = [1, 1, 1, 1, -8, 1, 1, 1, 1]
    datos_laplace = foto.filter(ImageFilter.Kernel((3,3), coeficientes, 1)).getdata()
    #datos de la imagen
    datos_imagen = foto.getdata()
    #factor de escalado
    w = 1 / 2
    #datos de imagen menos datos de Laplace escalados
    datos_nitidez = [datos_imagen[x] - (w * datos_laplace[x]) for x in range(len(datos_laplace))]
    imagen_nitidez = Image.new('L', foto.size)
    imagen_nitidez.putdata(datos_nitidez)
    imagen_nitidez.save(path)
    foto.close()
    imagen_nitidez.close()

    #ENVIANDOLA A GOOGLE CLOUD
    vision_client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)
        response = vision_client.text_detection(image=image)

    texts = response.text_annotations
    cont = 0
    text_acum = ""
    for text in texts:
        if cont > 0: 
            text_acum += text.description + " "
        cont = cont + 1

    print(text_acum)

    tts = gTTS(text=text_acum,lang='es')
    tts.save("audios_generados/texto.mp3")
    os.system("mpg321 audios_generados/texto.mp3")
except Exception as e:
    print("Error de internet: {0}".format(e))
    os.system("mpg321 audios_definidos/algo_mal.mp3")
