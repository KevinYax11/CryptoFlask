import os
import base64
from .config import Config
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

KEYS_DIR = Config.KEYS_DIR

def generar_y_guardar_claves(base_name):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    priv_path = os.path.join(KEYS_DIR, f"{base_name}_private.pem")
    pub_path = os.path.join(KEYS_DIR, f"{base_name}_public.pem")
    
    with open(priv_path, "wb") as f:
        f.write(pem_private)
    with open(pub_path, "wb") as f:
        f.write(pem_public)
    
    return priv_path, pub_path

def cargar_clave_publica(base_name):
    path = os.path.join(KEYS_DIR, f"{base_name}_public.pem")
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def cargar_clave_privada(base_name):
    path = os.path.join(KEYS_DIR, f"{base_name}_private.pem")
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def cifrar_mensaje(message_bytes, key_name):
    public_key = cargar_clave_publica(key_name)
    encrypted = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

def descifrar_mensaje(encrypted_b64_str, key_name):
    encrypted_message_bytes = base64.b64decode(encrypted_b64_str)
    private_key = cargar_clave_privada(key_name)
    
    decrypted_bytes = private_key.decrypt(
        encrypted_message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_bytes.decode('utf-8')

def firmar_mensaje(message_bytes, key_name):
    private_key = cargar_clave_privada(key_name)
    
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return base64.b64encode(signature).decode('utf-8')

def verificar_firma(message_bytes, signature_b64_str, key_name):
    signature_bytes = base64.b64decode(signature_b64_str)
    public_key = cargar_clave_publica(key_name)
    
    try:
        public_key.verify(
            signature_bytes,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False