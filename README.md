# Api Prueba Tecnica Coppel

Api REST para el manejo de usuarios y productos


## Características

+ Backend de FastAPI en Python.
+ Base de datos PostgreSQL
+ Alembic migrasion de base de datos.

## Uso de la aplicación

Para poder darle uso a la aplicacion se debe clonar la aplicacion, a lo que se debe seguir los siguientes pasos:

1. Clonar el repositorio:

2. Abre el proyecto en vscode y usa el devcontainer para trabajar en un ambiente aislado. (Necesitas la extensión de Remote - Containers de vscode)

    2.1. Si no quieres usar el devcontainer, crea un entorno virtual de Python:

    ```console
    python3 -m venv venv
     ```

3. Instala los módulos listados en el archivo `requirements.txt`:

    ```console
    pip3 install -r requirements.txt
    ```

4. Inicia la aplicación:

    ```console
    python main.py
    ```

Cuando se ejecuta la aplicacion esta escuchando en el puerto 8080 en la dirección [0.0.0.0](0.0.0.0:8080).

Pero si se esta usando lo que seria e puerto 8080 puede cambiarlo por cualquiera de los puertos que no se esten ocupando como en este que esta escuchando en el 8082.