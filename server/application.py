#!/usr/bin/python3

# Import packages
from flask import Flask, request, abort, Response, jsonify
from api.rec_img import reconImg
from api.speech_synthesis import speechSynthesis as textToSpeech
from api.rekognition import compare_conjunto
import matplotlib.image as mpimg
import cv2
import numpy as np
import flask


# import matplotlib.pyplot as plt
# Create Flask application
application = Flask(__name__)


# api/speech-synthesis endpoint
@application.route('/api/speech-synthesis', methods=['POST'])
def speechSynthesis():
    try:
        textToSpeech()
    except Exception as error:
        print(error)
        abort(400)
    return Response(status=200)

# metodo de reconocimiento de bordes
@application.route('/api/img', methods=['POST'])
def imgReco():
    try:
        #read image file string data
        filestr = request.files['file'].read()
        #convert string data to numpy array
        file_bytes = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

        #process image
        bytes_str = reconImg(img)
        # Encode the resized image to PNG
        _, im_bytes_np = cv2.imencode('.jpg', img)
        # Constuct raw bytes string 
        bytes_str = im_bytes_np.tobytes()
        # Create response given the bytes
        response = flask.make_response(bytes_str)
        response.headers.set('Content-Type', 'image/jpg')
        
    except Exception as error:
        print(error)
        abort(400)
    return response

# llamar a la api Rekognition
@application.route('/api/rekognition', methods=['POST'])
def findFaces():
    try:
        # recoger datos de curl
        filestr = request.files['file'].read()
        bucketName= 'dvlbucket01'
        imageName= 'images/PXL_20221125_154355477.jpg'
        
        # bucketName= request.files['bucketName']
        # imageName= request.files['imageName']
        # print(bucketName)
        # print(imageName)

        # llamar a metodo de rekognition para comparar caras
        face_matches=compare_conjunto(filestr, bucketName)
        print("Face matches: " + str(face_matches))
        if (face_matches!=0):
            respuesta='Coincidencias: '+ str(face_matches) + '\nLas imagenes procesadas se han guardado y comprimido correctamente\n'
        else:
            respuesta='No han habido coincidencias\n'
        response = flask.make_response(respuesta)
        
    except Exception as error:
        print(error)
        abort(400)
    return response
 


# Run the app
if __name__ == "__main__":
    
    
    #plt.imshow(imgReco())
     application.debug = True
     application.run() # Running on http://127.0.0.1:5000/
    # curl -X POST localhost:5000/api/speech-synthesis
    # curl -F "file=@prueba.jpg" http://localhost:5000/api/img
    # curl -F "file=@prueba.jpg" --output '/home/ruben/Descargas/result.jpg' http://localhost:5000/api/img