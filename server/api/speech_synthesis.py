#!/usr/bin/python3

# Import packages
import boto3, os
from dotenv import load_dotenv

# Take environment variables from .env file
load_dotenv()

# Get env variables
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
region = os.environ.get('REGION1')
bucketName = os.environ.get('BUCKET_NAME1')

# Create the service Polly and assign credentials
polly_client = boto3.Session(
    aws_access_key_id=accessKeyId,                  
    aws_secret_access_key=secretKey,
    region_name=region).client('polly')

def speechSynthesis():
    # Create parameters and call the service
    try:
        response = polly_client.start_speech_synthesis_task(
            Engine='neural',
            LanguageCode='es-ES', 
            OutputFormat='mp3',
            OutputS3BucketName=bucketName,
            OutputS3KeyPrefix='RubenAplicacionPython',
            Text='<speak><s>¿En qué se parece una suegra a un nubarrón?</s><s>En que cuando se marchan se queda una buena tarde</s></speak>',
            TextType='ssml',
            SampleRate='22050',
            VoiceId='Lucia')

        print("Audio file is saved into {} ".format(response['SynthesisTask']['OutputUri']))
    except:
        raise Exception("Oops! An unexpected error was raised")


# if __name__ == "__main__":
#     speechSynthesis()
