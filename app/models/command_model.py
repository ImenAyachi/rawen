import subprocess
import shlex

def run_command(cmd):
    try:
        args = shlex.split(cmd)
        args = ["sudo"] + args
        result = subprocess.run(args, capture_output=True, text=True)
        success = (result.returncode == 0)
        output = result.stdout or ""
        error = result.stderr or ""
        return success, output, error
    except FileNotFoundError:
        return False, "", "Commande introuvable."
    except Exception as e:
        return False, "", f"Erreur : {str(e)}"