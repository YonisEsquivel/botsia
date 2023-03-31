# Botsia

Botsia es un bot para operaciones de trading con criptomonedas en Binance. El bot actualmente funciona en modo Spot y está en desarrollo para su uso en modo Futuros.

## Requerimientos de instalación
- Crear un entorno virtual con `virtualenv env`
- Activar el entorno virtual con `env\Scripts\activate.bat`
- Instalar las dependencias con `pip install requirements.txt`
- Establecer la variable de entorno `FLASK_DEBUG` en `development`
- Cargar la base de datos MySQL que se encuentra en la carpeta `db`

## Uso del Bot
Para configurar el bot, es necesario editar el archivo `config.py` y establecer los parámetros iniciales. En la sección de Spot el bot funciona muy bien y se puede utilizar sin problemas. Además, se ha creado un link de configuración para no tener que hacer cambios directamente en el código, aunque aún no está conectado a la base de datos.

La sección de futuros aún está en desarrollo y se irá actualizando conforme se vayan considerando las variables relevantes para su uso.

## Contribuciones
Este proyecto es colaborativo y se agradecen las contribuciones al código explicando de forma clara cada línea de código en una rama aparte con su identificación. Juntos podemos mejorar Botsia y obtener mejores resultados en nuestras operaciones de trading.

# ¡Juntos podemos ganar!
