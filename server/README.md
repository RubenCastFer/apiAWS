## Instrucciones para la ejecución del ejemplo

### Pasos

1. python3 -m virtualenv .
2. Reemplaza los tokens de cuenta de AWS en el archivo .env
3. source bin/activate
4. pip3 install -r requirements.txt
5. python3 application.py
6. Abre otro terminal y ejecuta: curl -H "Content-Type: application/json" -X POST -d '{"voiceId": "Lucia", "text": "Servidor Flask con funcionalidad de texto a voz"}' localhost:5000/api/speech-synthesis