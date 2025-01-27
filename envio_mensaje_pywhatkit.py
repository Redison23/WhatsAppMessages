import pywhatkit as pwk
from datetime import datetime

# Datos del mensaje
listaTelefonos = ["", "312321312", "542342423"]

for numero in listaTelefonos:
    telefono = f"+57{numero}"  # Número de WhatsApp (con código de país)
    mensaje = "Hola, este es un mensaje de prueba enviado con Python."  # Mensaje a enviar

    # Obtener la hora actual
    hora_actual = datetime.now()
    hora_envio = hora_actual.hour
    minuto_envio = hora_actual.minute + 1  # Programar el envío para el siguiente minuto


    # Enviar el mensaje08

    try:
        pwk.sendwhatmsg(telefono, mensaje, hora_envio, minuto_envio, 10, True, 30)
        print(f"Mensaje enviado a {telefono}")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")


