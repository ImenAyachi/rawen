from flask import Blueprint, render_template, request
from app.models.command_model import run_command

command_bp = Blueprint("command", __name__, url_prefix="/command")

@command_bp.route("/", methods=["GET", "POST"])
def execute_command():
    output = ""
    error_message = ""
    user_command = ""

    if request.method == "POST":
        user_command = request.form.get("command", "")
        if user_command.strip() == "":
            error_message = "Veuillez saisir une commande."
        else:
            success, out, err = run_command(user_command)
            output = out
            error_message = err

    return render_template("command.html", user_command=user_command, output=output, error_message=error_message)
