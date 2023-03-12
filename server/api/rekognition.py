#!/usr/bin/python3

# Import packages
import boto3, os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
import base64
import io
import shutil
import zipfile



# Take environment variables from .env file
load_dotenv()

# Get env variables
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
region = os.environ.get('REGION')
bucketName = os.environ.get('BUCKET_NAME1')

# Create the service Rekognition and assign credentials
rekognition_client = boto3.Session(
    aws_access_key_id=accessKeyId,                  
    aws_secret_access_key=secretKey,
    region_name=region).client('rekognition')

# Create connection to Wasabi / S3
s3 = boto3.Session(
    aws_access_key_id=accessKeyId,                  
    aws_secret_access_key=secretKey,
    region_name=region).client('s3')


def boundingBoxes(bucketName, imageName, response):

    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucketName,imageName)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)

    # medidas de la imagen
    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)  

    # posicion de la cara
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(round(faceMatch['Similarity'],5))+'%'
        
        # coger los puntos para poder dibujarlos
        box = position
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']

        points = (
            (left,top),
            (left + width, top),
            (left + width, top + height),
            (left , top + height),
            (left, top)

        )

        # dibujar sobre la cara y guardar la imagen 
        font = ImageFont.truetype("Ubuntu-R.ttf", size=40)
        draw.line(points, fill='yellow', width=10)
        draw.text((left + width+10,top),'Matches\n'+similarity, font=font, fill ='yellow')
        # image.show()
        image.save(imageName)
        
def compare_faces(sourceFile, bucketName, imageName):

    # imagen almacenada en s3
    s3 = boto3.resource('s3', region_name='us-east-2')
    bucket = s3.Bucket(bucketName)
    object = bucket.Object(imageName)
    response = object.get()
    file_stream = response['Body']
    

    # client=boto3.client('rekognition')
   
    # abre las imagenes
    # with open(sourceFile, 'rb') as source_image:
    #     source_bytes = base64.b64encode(source_image.read())

    # imageSource=open(sourceFile,'rb')
    #imageTarget=open(targetFile,'rb')
    
    # Llamar a rekognition y realizar la comparacion
    response=rekognition_client.compare_faces(SimilarityThreshold=80,
                                # SourceImage={'Bytes': imageSource.read()},
                                SourceImage={'Bytes': sourceFile},
                                # TargetImage={'Bytes': imageTarget.read()})
                                TargetImage={'Bytes': file_stream.read()})
    
    # dibujar el cuadro sobre la cara
    if(len(response['FaceMatches'])!=0):
        boundingBoxes(bucketName, imageName, response)
    
    # for faceMatch in response['FaceMatches']:
    #     position = faceMatch['Face']['BoundingBox']
    #     similarity = str(faceMatch['Similarity'])
    #     print('The face at ' +
    #            str(position['Left']) + ' ' +
    #            str(position['Top']) +
    #            ' matches with ' + similarity + '% confidence')

    # Cerrar imagenes
    #imageSource.close()
    #imageTarget.close()     
    return len(response['FaceMatches'])          


def compare_conjunto(source_file, bucketName):

    # lista con imagenes almacenada en s3
    s3 = boto3.resource('s3', region_name='us-east-2')
    bucket = s3.Bucket(bucketName)
    objs = bucket.objects.filter(Prefix='images/', Delimiter='/').all()
    
    # numero de imagenes que aparece la cara a comparar
    coincidenciasImg=0


    directorio=''
    # bucle para procesar la imagenes
    for obj in objs:
        print(obj.key)

        # cuando el objeto no sea la carpeta llamar a comparar 
        if(obj.key!='images/'):
            # numero de coincidencias en una imagen, puede ser mas de 1
            coincidencias = compare_faces(source_file, bucketName, obj.key)
            if(coincidencias!=0):
                coincidenciasImg+=1
        else:
            directorio=obj.key
            os.mkdir(directorio)

    
    # comprimir el archivo y borrar la carpeta
    if(os.path.exists(directorio)):
        fantasy_zip = zipfile.ZipFile('img/imagenes.zip', 'w')
        
        for folder, subfolders, files in os.walk(directorio):
        
            for file in files:
                fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), directorio), compress_type = zipfile.ZIP_DEFLATED)
        
        fantasy_zip.close()       
        shutil.rmtree(directorio)
        
    return coincidenciasImg

def main():
    # rutas de las imagenes
    source_file='/home/ruben/Descargas/IMG_00731.jpg'
    target_file='/home/ruben/Descargas/PXL_20221125_154355477.jpg'
    # face_matches=compare_faces(source_file, target_file)
    
    bucketName= 'dvlbucket01'
    imageName= 'images/PXL_20221125_154355477.jpg'
    # face_matches=compare_faces(source_file, bucketName, imageName)
    face_matches = compare_conjunto(source_file, bucketName)
    print("Face matches: " + str(face_matches))


# if __name__ == "__main__":
#      main()


# def speechSynthesis():
#     # Create parameters and call the service
#     try:
#         response = 

#         print("Audio file is saved into {} ".format(response['SynthesisTask']['OutputUri']))
#     except:
#         raise Exception("Oops! An unexpected error was raised")
