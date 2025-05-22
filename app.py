from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, make_response, send_file
from flask_mail import Mail, Message
from FeatureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model
from spam_predictor import predict_spam  # ✅ On garde seulement l'import
import traceback
from sql_injection import is_sql_injection
from flask_cors import CORS
import socket
import threading
import ipaddress
from weakpassword import is_password_strong, generate_strong_password
import random
import string
from geminichat import ask_gemini
from cryptography.fernet import Fernet
from chiffrement import *
from virustotal import scan_file_virustotal
import os
from portdetection import scan_ports

app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv('SECRET_KEY')

# Configuration des emails en lisant depuis .env
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))  # doit être un entier
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)
# Charger le modèle de détection de phishing
model = load_model('model/phishingdetection')
print("Colonnes attendues :", model.feature_names_in_)


def predict(url):
    # Extraction des caractéristiques de l'URL
    data = featureExtraction(url)

    # Effectuer la prédiction
    result = predict_model(model, data=data)

    # Obtenir le score et l'étiquette de la prédiction
    prediction_score = result['prediction_score'][0]
    prediction_label = result['prediction_label'][0]

    # Conversion explicite pour s'assurer que ces valeurs sont sérialisables en JSON
    prediction_score = float(prediction_score)  # Convertir en float
    prediction_label = int(prediction_label)    # Convertir en int

    return {
        'prediction_label': prediction_label,
        'prediction_score': prediction_score * 100,
    }


# ===================== ROUTES =====================

@app.route('/')
def index():
    # Get cookie values with defaults
    accepted_cookies = request.cookies.get('accepted_cookies', None)
    langue = request.cookies.get('langue', 'fr')
    theme = request.cookies.get('theme', 'light')
    
    # Flag to check if the cookie bar should be shown
    show_cookie_bar = accepted_cookies is None  # Show if the cookie is not accepted yet

    # Debugging logs
    print(f"accepted_cookies: {accepted_cookies}")
    print(f"langue: {langue}")
    print(f"theme: {theme}")
    print(f"show_cookie_bar: {show_cookie_bar}")

    return render_template('index.html', 
                         accepted_cookies=accepted_cookies,
                         langue=langue,
                         theme=theme,
                         show_cookie_bar=show_cookie_bar)


@app.route('/accept_cookies', methods=['POST'])
def accept_cookies():
    langue = request.form.get('langue', 'fr')
    theme = request.form.get('theme', 'light')

    resp = make_response(redirect('/'))
    resp.set_cookie('accepted_cookies', 'yes', max_age=31536000)  # 1 year
    resp.set_cookie('langue', langue, max_age=31536000)
    resp.set_cookie('theme', theme, max_age=31536000)

    print("Cookies accepted and set.")
    return resp


@app.route('/reject_cookies', methods=['POST'])
def reject_cookies():
    resp = make_response(redirect('/'))
    resp.set_cookie('accepted_cookies', 'no', max_age=31536000)

    print("Cookies rejected and deleted.")
    return resp


@app.route('/update_theme', methods=['POST'])
def update_theme():
    theme = request.form.get('theme', 'light')
    resp = make_response('', 204)  # No content
    resp.set_cookie('theme', theme, max_age=31536000)
    return resp


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/phishing-check", methods=["GET", "POST"])
def phishing_check():
    data = None
    if request.method == "POST":
        url = request.form["url"]
        data = predict(url)
        return render_template('phishing_detection.html', url=url, data=data)
    return render_template("phishing_detection.html", data=data)


@app.route("/spam-check", methods=["GET", "POST"])
def spam_check():
    result = None
    message = ""
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message:
            is_spam = predict_spam(message)
            result = "Spam détecté ❌" if is_spam else "Aucun spam détecté ✅"
        else:
            flash("Veuillez entrer un message à analyser.", "warning")
    return render_template("check_spam.html", result=result, message=message)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            msg = Message(f"Message de {name}", recipients=["imen333ay@gmail.com"])
            msg.body = f"Nom: {name}\nEmail: {email}\nMessage: {message}"
            try:
                mail.send(msg)
                return redirect(url_for('contact_success'))
            except Exception:
                return redirect(url_for('contact'))
        else:
            flash("Veuillez remplir tous les champs.", 'danger')
            return redirect(url_for('contact'))

    return render_template("contact.html")


@app.route('/contact-success')
def contact_success():
    return render_template('success.html')



@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    response = None
    question = None
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        response = ask_gemini(question)  # Use Gemini API to get dynamic response
    
    return render_template("chatbot.html", question=question, response=response)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/phishing")
def phishing():
    return render_template("phishing.html")


@app.route("/sql-injection", methods=["GET", "POST"])
def sql_injection_route():
    result = None
    input_text = ""
    
    if request.method == "POST":
        input_text = request.form.get("input_text", "").strip()
        
        if input_text:
            if is_sql_injection(input_text):
                result = "SQL Injection detected ❌"
            else:
                result = "No SQL Injection detected ✅"
        else:
            flash("Veuillez entrer une entrée à analyser.", "warning")
    
    return render_template("sql_injection.html", result=result, input_text=input_text)



# ✅ Route API pour l'extension Chrome
@app.route('/predict', methods=['POST'])
def predict_api():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Aucune URL fournie'}), 400

    try:
        url = data['url']
        prediction = predict(url)

        # Convertir la prédiction en JSON sérialisable
        response = jsonify(prediction)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    

def is_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


@app.route('/port-scanner', methods=['GET', 'POST'])
def port_scanner():
    results = []
    if request.method == 'POST':
        target = request.form['target'].strip()
        results = scan_ports(target, 1000)  # ou une autre valeur si tu veux plus de ports

    return render_template('port_scanner.html', results=results)


@app.route('/check-password', methods=['GET', 'POST'])
def check_password():
    result = None
    generated_password = None

    if request.method == 'POST':
        password = request.form.get('password')
        action = request.form.get('action')

        if password:
            if action == 'check_password':
                result = is_password_strong(password)
            elif action == 'generate_password':
                generated_password = generate_strong_password(password)

    return render_template('check_password.html', result=result, generated_password=generated_password)


@app.route('/aes', methods=['GET', 'POST'])
def aes():
    result = None
    original = ""
    key = ""
    action = ""

    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        action = request.form['action']
        original = text

        if is_fernet_key(key):
            try:
                if action == 'encrypt':
                    result = encrypt_with_fernet(key, text)
                elif action == 'decrypt':
                    result = decrypt_with_fernet(key, text)
            except Exception as e:
                result = f"Erreur Fernet : {e}"
        else:
            try:
                if action == 'encrypt':
                    result = encrypt_with_aes(key, text)
                elif action == 'decrypt':
                    result = decrypt_with_aes(key, text)
            except Exception as e:
                result = f"Erreur AES : {e}"

    return render_template('aes.html', result=result, original=original, key=key, action=action)

@app.route('/generate-key')
def generate_key():
    return generate_fernet_key()


@app.route('/scan-file', methods=['GET', 'POST'])
def scan_file():
    result = None
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename != '':
            result = scan_file_virustotal(uploaded_file.stream, uploaded_file.filename)
        else:
            result = {"error": "No file selected"}
    return render_template('scan_file.html', result=result)


# Page d'information sur l'extension
@app.route('/extension-info')
def extension_info():
    return render_template('extension_info.html')

# Route pour télécharger réellement l'extension (par exemple un fichier .zip ou .crx)
@app.route('/download-extension')
def download_extension():
    return send_file('static/phishing detector extension.zip', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)