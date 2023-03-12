#!/usr/bin/python3

# Import packages
import boto3, os
#from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from dotenv import load_dotenv

# Take environment variables from .env file
load_dotenv()

# Get env variables
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
region = os.environ.get('REGION1')
bucketName = os.environ.get('BUCKET_NAME1')

def reconImg(img):
    # Create parameters and call the service
    try:
        
        # Convertimos a escala de grises
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Aplicar suavizado Gaussiano
        gauss = cv2.GaussianBlur(gris, (5,5), 0)
        # plt.imshow(gauss)
        
        # Detectamos los bordes con Canny
        canny = cv2.Canny(gauss, 50, 150)
        # plt.imshow(canny)
        
        # Buscamos los contornos
        (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        img=cv2.drawContours(img,contornos,-1,(0,0,255), 2)
  
        return img
    except:
        raise Exception("Oops! An unexpected error was raised")



# if __name__ == "__main__":
    # img = mpimg.imread('../img/moneda.jpg')
    #  reconImg()
