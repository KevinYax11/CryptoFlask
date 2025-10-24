# CryptoFlask
Web app in Python to encrypt, decrypt, sign, and verify messages or files using RSA. Includes key management and digital signature features through an intuitive interface.

**Kevin Miguel Yax Puác**
**1529422**
**Estructura De Datos II**

*# Guía de Ejecución - CryptoFlask*

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repositorio>
cd CryptoFlask
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, instala manualmente:
```bash
pip install flask cryptography
```

## Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`


## Estructura de Carpetas Requerida

```
CryptoFlask/
├── app.py
├── project/
│   ├── __init__.py
│   ├── config.py
│   ├── crypto.py
│   └── routes.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── keys.html
│   ├── encrypt.html
│   ├── decrypt.html
│   ├── sign.html
│   └── verify.html
├── static/
│   └── style.css
└── keys/  (se crea automáticamente)
```

## Verificar Instalación

Una vez iniciada la aplicación, deberías ver:

```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

Abre tu navegador y ve a `http://localhost:5000`
