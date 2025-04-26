from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clef_secrete'  # nécessaire si on utilise flash() ou des sessions

# Enregistrer les blueprints des contrôleurs
from app.controllers import vpn_controller, command_controller
app.register_blueprint(vpn_controller.vpn_bp)
app.register_blueprint(command_controller.command_bp)