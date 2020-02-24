# API-Sentiment


_En esta API, se pueden crear un chat con todos sus elementos y, una vez creado, analizar todos los sentimientos de su contenido_

## Comienzo 🚀


_El análisis pormenorizado del funcionamiento se sitúa en el archivo 'main.ipynb'_

_El resto de carpetas siguen la denominación estándar para el tipo de datos que poseen,y no requieren aclaraciones adicionales._


## Uso de 'main.py' 🔧


* **Inicio:**

_Ejecucion de programa:'path/python3 main.py'_

_Ejecución de Informe en Jupyter Notebook: 'path/jupyter-notebook Demo.py'_


## Operaciones básicas ✒️

* **Añadir usuario** - */user/create/<username>* - (Ej: "http://0.0.0.0:4500/user/create/Marcos")

* **Crear Chat** - */chat/create* - (Ej: "http://0.0.0.0:4500/chat/create/?usernames=Pablo,Juan,Marcos")

* **Añadir usuario a chat** - */chat/<chat_id>/adduser* - (Ej: "http://0.0.0.0:4500/chat/0/adduser?username=Laura")

* **Añadir mensaje a chat** - */chat/<chat_id>/addmessage* - (Ej: "http://0.0.0.0:4500/chat/0/addmessage?username=Juan")


## Respuestas básicas ✒️

* **Obtención de mensajes de un chat** - */chat/<chat_id>/list* - (Ej: "http://0.0.0.0:4500/chat/0/list")

* **Reporte de sentimientos de un chat** - */chat/<chat_id>/sentiment* - (Ej: "http://0.0.0.0:4500/chat/0/sentiment")

* **Recomendación de usuarios** - */user/<user_id>/recommend* - (Ej: "http://0.0.0.0:4500/user/0/recommend")


## Construido con 🛠️

* [Jupyter Notebook](https://jupyter.org/) - Herramienta principal
* [Flask](https://palletsprojects.com/p/flask/) - Manipulación de Requests
* [MongoDB](https://www.mongodb.com/) - Manipulación de Databases








