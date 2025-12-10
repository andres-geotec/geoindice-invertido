# Indice invertido

Este programa crea un ídice invertido para optimizar las consultas mediante tokens y calculando un ranking de relevancia textual (TF-IDF).

- Autor: **Andrés Martínez González**

## Comandos para preparar la ejecución del programa

### Creación de entorno virtual
```sh
python3 -m venv .venv
```

### Activación de entorno virtual
```sh
source .venv/bin/activate
```

### Instalación de dependencias
```sh
pip install -r requirements.txt
```

## Comandos para ejecutar el programa

### Actualización/Generación de documentos, tokens e índices
```sh
python manage.py fetch_resources
```

### Ejecución del servicio
```sh
python manage.py runserver
```
