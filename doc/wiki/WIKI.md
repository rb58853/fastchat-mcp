# FastChat-MCP Wiki

Bienvenido a la documentación oficial de **FastChat-MCP**. Este repositorio proporciona una solución robusta y flexible para la gestión de chats locales y remotos, orientada tanto a usuarios finales como a desarrolladores que deseen integrar o extender sus funcionalidades.

---

## Tabla de Contenidos

- [Introducción](#introducción)
- [Instalación](#instalación)
- [Uso Básico](#uso-básico)
- [Clase `Chat`](#clase-chat)
  - [Características](#características)
  - [Ejemplo de Uso](#ejemplo-de-uso)
- [Función `open_local_chat`](#función-open_local_chat)
  - [Parámetros](#parámetros)
  - [Ejemplo de Uso](#ejemplo-de-uso-1)
- [Ventajas](#ventajas)
- [Casos de Uso](#casos-de-uso)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Introducción

**FastChat-MCP** es un paquete diseñado para facilitar la creación, gestión y extensión de sesiones de chat, permitiendo tanto la interacción local como la integración con sistemas externos. Su arquitectura modular permite a los desarrolladores personalizar y ampliar sus capacidades según las necesidades del proyecto.

---

## Instalación

```bash
pip install fastchat-mcp
```

O bien, clona el repositorio y usa:

```bash
python setup.py install
```

---

## Uso Básico

El flujo típico consiste en crear una instancia de la clase `Chat` y utilizar la función `open_local_chat` para iniciar una sesión de chat local.

---

## Clase `Chat`

La clase principal del paquete. Encapsula toda la lógica relacionada con la gestión de sesiones de chat, almacenamiento de mensajes, historial y configuración de la conversación.

### Características

- **Gestión de mensajes:** Envía, recibe y almacena mensajes.
- **Historial:** Permite acceder y manipular el historial de la conversación.
- **Configuración flexible:** Personaliza parámetros como el modelo de IA, temperatura, longitud de respuesta, etc.
- **Extensible:** Fácil de heredar y extender para casos de uso avanzados.

### Ejemplo de Uso

```python
from fastchat_mcp import Chat

# Crear una nueva sesión de chat
chat = Chat(model="gpt4-o-mini")

query:str = "Hola, ¿En que puedes ayudarme?"
for step in chat(query):
    print(f"{step.response}", end="")
        
```

---

## Función `open_local_chat`

Función utilitaria para iniciar una sesión de chat local de manera rápida y sencilla.

### Parámetros

- `model` (str): Modelo de IA a utilizar.
- `temperature` (float): Controla la aleatoriedad de las respuestas.
- `max_tokens` (int): Máximo de tokens por respuesta.
- Otros parámetros opcionales según la configuración deseada.

### Ejemplo de Uso

```python
from fastchat_mcp import open_local_chat

# Iniciar un chat local con configuración personalizada
session = open_local_chat(model="gpt-3.5-turbo", temperature=0.5)
session.send("¿Cuál es la capital de Francia?")
```

---

## Ventajas

- **Fácil de usar:** API intuitiva y bien documentada.
- **Flexible:** Admite personalización y extensión.
- **Integración sencilla:** Compatible con otros sistemas y flujos de trabajo.
- **Soporte para múltiples modelos:** Cambia de modelo fácilmente según tus necesidades.

---

## Casos de Uso

- **Desarrollo de asistentes virtuales personalizados.**
- **Integración en plataformas de atención al cliente.**
- **Prototipado rápido de interfaces conversacionales.**
- **Análisis y procesamiento de conversaciones.**

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor, revisa las [guidelines de contribución](CONTRIBUTING.md) antes de enviar un pull request.

---

## Licencia

Este proyecto está licenciado bajo los términos de la [MIT License](LICENSE).

---

¿Tienes dudas o sugerencias? ¡Abre un issue o contacta a los mantenedores!
