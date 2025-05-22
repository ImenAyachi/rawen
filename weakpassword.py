import re
import random
import string

def is_password_strong(password: str) -> str:
    issues = []

    if len(password) < 8:
        issues.append("au moins 8 caractères")
    if not re.search(r"[A-Z]", password):
        issues.append("une lettre majuscule")
    if not re.search(r"[a-z]", password):
        issues.append("une lettre minuscule")
    if not re.search(r"[0-9]", password):
        issues.append("un chiffre")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("un caractère spécial")

    if not issues:
        return "Mot de passe fort ✅"
    else:
        return "Mot de passe faible ❌ – Il manque : " + ", ".join(issues) + "."

def generate_strong_password(base_password: str, length: int = 12) -> str:
    required = []

    if not re.search(r"[A-Z]", base_password):
        required.append(random.choice(string.ascii_uppercase))
    if not re.search(r"[a-z]", base_password):
        required.append(random.choice(string.ascii_lowercase))
    if not re.search(r"[0-9]", base_password):
        required.append(random.choice(string.digits))
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", base_password):
        required.append(random.choice("!@#$%^&*(),.?\":{}|<>"))

    all_chars = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"

    while len(base_password + ''.join(required)) < length:
        required.append(random.choice(all_chars))

    combined = list(base_password + ''.join(required))
    random.shuffle(combined)
    return ''.join(combined)
