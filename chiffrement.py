from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

# Génère une clé Fernet (44 caractères)
def generate_fernet_key():
    return Fernet.generate_key().decode()

# Vérifie si la clé est compatible avec Fernet
def is_fernet_key(key):
    return len(key) == 44 and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in key)

# --- Méthodes avec Fernet ---
def encrypt_with_fernet(key, text):
    f = Fernet(key.encode())
    return f.encrypt(text.encode()).decode()

def decrypt_with_fernet(key, encrypted_text):
    f = Fernet(key.encode())
    return f.decrypt(encrypted_text.encode()).decode()

# --- Méthodes avec AES personnalisé (clé manuelle) ---
def derive_aes_key(user_key):
    return hashlib.sha256(user_key.encode()).digest()

def encrypt_with_aes(user_key, plain_text):
    key = derive_aes_key(user_key)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode()
    ct = base64.b64encode(ct_bytes).decode()
    return iv + ":" + ct

def decrypt_with_aes(user_key, encrypted_text):
    key = derive_aes_key(user_key)
    try:
        iv, ct = encrypted_text.split(":")
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size).decode()
        return pt
    except Exception as e:
        return f"Erreur de déchiffrement : {e}"
