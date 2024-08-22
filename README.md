# SSCarFight

SSCarFight es un juego simple desarrollado en Python utilizando la biblioteca Pygame. En este juego, el jugador controla un coche que debe enfrentarse a un jefe en una carrera/batalla épica.

## Funcionalidades

- **Movimiento del jugador**: El jugador puede mover su coche utilizando las teclas de flechas y disparar con la recla "Q".
- **Movimiento del jefe**: El jefe se mueve y dispara automaticamente.
- **Menú**: El juego incluye un menú inicial que permite al jugador iniciar el juego, consultar por los controles y salir del juego.

## Requisitos

- Python 3.x
- Pygame

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/tu_usuario/SSCarFight.git
    ```
2. Navega al directorio del proyecto:
    ```sh
    cd SSCarFight
    ```
3. Instala las dependencias:
    ```sh
    pip install pygame
    ```

## Ejecución

Para ejecutar el juego, simplemente corre el archivo `main.py`:
    ```sh
    python src/main.py
    ```
## Cómo Jugar

- **Mover el coche**: Usa las teclas de flechas para mover el coche.
- **Disparar:**: Presiona la tecla "Q" para disparar balas.
- **Objetivo**: Llega primero a la línea de meta o destruye al jefe para ganar.

## Estructura del Proyecto

- **src/**: Contiene el código fuente del juego.
   - **main.py**: Archivo principal que inicia el juego.
   - **player.py**: Contiene la clase Player que maneja el comportamiento del jugador.
   - **boss.py**: Contiene la clase Boss que maneja el comportamiento del jefe.
   - **menu.py**: Contiene la clase Menu que maneja el menú del juego.
   - **bullet.py**: Contiene la clase Bullet que maneja las balas disparadas por el jugador y el jefe.
- **assets/**: Contiene los recursos del juego como imágenes y sonidos.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
3. Realiza tus cambios y haz commit (git commit -am 'Añadir nueva funcionalidad').
4. Sube tus cambios a tu rama (git push origin feature/nueva-funcionalidad).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. 