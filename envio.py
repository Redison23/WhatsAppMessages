#Requests is for send the POST request
import requests
#pandas is for manage the data of the users
import pandas as pd
#This is my library for manage the Database connection
import conectDB
#Datetime is for manage dates
from datetime import datetime
#Is for .env file for security
from dotenv import load_dotenv
import os
import locale

#Charge .env file
load_dotenv()
#stablishment spanish as start language
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") 

#Variables
hostDB, nameDB, userDB, passwordDB, tableName, clinicName, clinicAdress, url, accessToken = (os.getenv("DB_HOST"), 
os.getenv("DB_DATABASE"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("TABLE_NAME"),
os.getenv("CLINIC_NAME"), os.getenv("CLINIC_ADRESS"), os.getenv("URL"), os.getenv("ACCESS_TOKEN"))

fechaActual = datetime.now().strftime('%Y-%m-%d')
conectar = conectDB.Connection(hostDB,nameDB, userDB, passwordDB)
conectar.connect()

results = conectar.select(f"""SELECT fecha, CONCAT(hora,' ', am_pm) AS hora, nombre, telefono AS numero
                          FROM {tableName}
                          WHERE fecha = %s;""", (fechaActual, ))
conectar.disconnect()
dataFrame = pd.DataFrame(results)
goodNumbers = dataFrame[(dataFrame["numero"].astype(str).str.len() == 10)]
#badNumbers = dataFrame[(dataFrame["numero"].astype(str).str.len() != 10)]

for row in goodNumbers.itertuples():
    
    #variables
    nombre = row.nombre
    dia = row.fecha.strftime("%A, %d de %B de %Y")
    hora = row.hora
    numero = row.numero

    # Datos del mensaje
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,  # Número de destino (formato internacional)
        "type": "template",
        "template": {
            "name": "recordatorio_citas",  # Nombre de la plantilla
            "language": {
                "code": "es",
                "policy": "deterministic"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        { "type": "text", "text": nombre },       # {1}
                        { "type": "text", "text": clinicName },    # {2}
                        { "type": "text", "text": dia },        # {3}
                        { "type": "text", "text": hora },       # {4}
                        { "type": "text", "text": clinicAdress },     # {5}
                        { "type": "text", "text": numero }     # {6}
                    ]
                }
            ]
        }
    }

    # Encabezados de la solicitud
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }
    try:
        # Realizar la solicitud POST
        response = requests.post(url, json=payload, headers=headers)
        # Verificar la respuesta
        if response.status_code == 200:
            print("Mensaje enviado con éxito:", response.json())
        else:
            print("Error al enviar el mensaje:", response.status_code, response.json())
    except:
        print("error")