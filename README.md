# Ronin Trading Bot

Este es un bot de trading para la blockchain Ronin que monitorea y ejecuta intercambios de tokens.

## Descripción General

El bot utiliza Web3.py para interactuar con la blockchain Ronin. Monitorea eventos de swap en la red y puede ejecutar trades automáticamente basados en ciertas condiciones.

## Estructura del Proyecto

- `main.py`: Contiene la lógica principal del bot, incluyendo funciones para mostrar balances, ejecutar trades, y monitorear eventos de swap.
- `config.py`: Configura la conexión a la blockchain Ronin y maneja las variables de entorno.
- `contracts.py`: Contiene las ABIs (Application Binary Interfaces) para los contratos inteligentes utilizados.
- `utils.py`: Proporciona funciones de utilidad para interactuar con los contratos y manejar direcciones de tokens.
- `requirements.txt`: Lista las dependencias del proyecto.
- `.env.example`: Ejemplo de archivo de variables de entorno.
- `tests/`: Contiene archivos de prueba.
- `utils/`: Contiene archivos de utilidad adicionales.

## Dependencias

Las dependencias del proyecto se encuentran en `requirements.txt`:
```
web3>=7.0
python-dotenv
requests
```

## Cómo Ejecutar el Proyecto

1. Asegúrate de tener Python instalado.
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno en un archivo `.env` basado en `.env.example`
4. Ejecuta el bot:
   ```
   python main.py
   ```

## Funcionalidades

- Monitorea eventos de swap en la red Ronin
- Ejecuta trades automáticamente basados en condiciones predefinidas
- Muestra balances de tokens y RON
- Detecta grandes ventas y compras de tokens específicos

## Contribuir

Si deseas contribuir a este proyecto, por favor sigue las siguientes pautas:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva feature'`)
4. Haz push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.