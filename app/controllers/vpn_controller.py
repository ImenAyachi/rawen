import subprocess
from flask import Blueprint, render_template, request

vpn_bp = Blueprint("vpn_bp", __name__,url_prefix="/vpn")
class IPTablesModel:
    @staticmethod
    def list_rules():
        """Liste les règles iptables (table filter par défaut)."""
        try:
            result = subprocess.run(
                ["sudo", "iptables", "-L", "-n", "-v"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Erreur lors de l'affichage des règles : {e.stderr}"

    @staticmethod
    def add_rule(rule):
        """
        Ajoute une règle iptables.
        Exemple : "-A INPUT -p tcp --dport 22 -j ACCEPT"
        """
        try:
            command = ["sudo", "iptables"] + rule.strip().split()
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout or "Règle ajoutée avec succès."
        except subprocess.CalledProcessError as e:
            return f"Erreur lors de l'ajout de la règle : {e.stderr}"
@vpn_bp.route('/', methods=['GET', 'POST'])
def vpn_home():
    # Exemple de données fictives
    config_data = "[Interface]\nPrivateKey = ...\nAddress = 10.0.0.1/24"
    status = "Inactif"
    message = ""

    return render_template("vpn.html", config_data=config_data, status=status, message=message)

    @staticmethod
    def delete_rule(rule):
        """
        Supprime une règle iptables.
        Exemple : "-D INPUT -p tcp --dport 22 -j ACCEPT"
        """
        try:
            command = ["sudo", "iptables"] + rule.strip().split()
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout or "Règle supprimée avec succès."
        except subprocess.CalledProcessError as e:
            return f"Erreur lors de la suppression de la règle : {e.stderr}"
