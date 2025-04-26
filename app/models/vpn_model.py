import subprocess

CONFIG_FILE = "/etc/wireguard/wg0.conf"
SERVICE_NAME = "wg-quick@wg0"

def get_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = ""
    except PermissionError:
        result = subprocess.run(["sudo", "cat", CONFIG_FILE], capture_output=True, text=True)
        content = result.stdout if result.returncode == 0 else ""
    return content

def save_config(new_config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(new_config)
        return True, "Configuration enregistrée."
    except PermissionError:
        result = subprocess.run(["sudo", "tee", CONFIG_FILE], input=new_config, text=True, capture_output=True)
        if result.returncode != 0:
            return False, result.stderr
        else:
            return True, "Configuration enregistrée (sudo)."
    except Exception as e:
        return False, f"Erreur : {e}"

def start_vpn():
    result = subprocess.run(["sudo", "systemctl", "start", SERVICE_NAME], capture_output=True, text=True)
    if result.returncode == 0:
        return True, "VPN démarré."
    else:
        return False, result.stderr

def stop_vpn():
    result = subprocess.run(["sudo", "systemctl", "stop", SERVICE_NAME], capture_output=True, text=True)
    if result.returncode == 0:
        return True, "VPN arrêté."
    else:
        return False, result.stderr

def get_status():
    result = subprocess.run(["sudo", "systemctl", "is-active", SERVICE_NAME], capture_output=True, text=True)
    return result.stdout.strip()
