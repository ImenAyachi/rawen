import os
from flask import Flask
from app.controllers.iptables_controller import iptables_bp
from app.controllers.vpn_controller import vpn_bp
from app.controllers.command_controller import command_bp

# Initialisation de l'application Flask
template_dir=os.path.abspath("app/templates")
app = Flask(__name__,template_folder=template_dir)

# Enregistrement des blueprints
app.register_blueprint(iptables_bp)
app.register_blueprint(vpn_bp)
app.register_blueprint(command_bp)

# Route racine (http://127.0.0.1:5000/)
@app.route("/")
def home():
    return """
    <h1>Bienvenue 👋</h1>
    <p>Accédez à :</p>
    <ul>
        <li><a href="/vpn">Gestion du VPN</a></li>
        <li><a href="/iptables">Gestion des règles iptables</a></li>
        <li><a href="/command">Exécution de commandes système</a></li>
    </ul>
    """

# Lancement du serveur
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=True)
