from flask import Blueprint, render_template, request, redirect
from app.models.iptables_model import IPTablesModel

# ✅ Correction : _name_ au lieu de name
iptables_bp = Blueprint("iptables_bp", __name__, url_prefix="/iptables")

@iptables_bp.route("/")
def show_iptables():
    rules = IPTablesModel.list_rules()
    return render_template("iptables.html", rules=rules)

@iptables_bp.route("/add", methods=["POST"])
def add_rule():
    rule = request.form["rule"]
    IPTablesModel.add_rule(rule)
    return redirect("/iptables")

@iptables_bp.route("/delete", methods=["POST"])
def delete_rule():
    rule = request.form["rule"]
    IPTablesModel.delete_rule(rule)
    return redirect("/iptables")
