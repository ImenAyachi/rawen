import pickle
import re
import os

# Charger le modèle spam.pkl
model_path = os.path.join(os.path.dirname(__file__), 'model', 'spam.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

def preprocess_message(message):
    """
    Prétraite le message : conversion en minuscules, suppression des liens, pièces jointes et caractères spéciaux.
    """
    # Convertir en minuscules
    message = message.lower()

    # Supprimer les liens
    message = re.sub(r'http[s]?://\S+', '', message)  # Supprimer les URL

    # Supprimer les pièces jointes (ex : "Téléchargez ici")
    message = re.sub(r'\b(téléchargez|pièce jointe|attachement)\b', '', message)

    # Supprimer les caractères spéciaux et les chiffres
    message = re.sub(r'[^a-zA-Z\s]', '', message)

    return message

def predict_spam(message: str) -> int:
    """
    Prédit si un message est un spam (1) ou non spam (0)
    """
    # Appliquer le prétraitement
    try:
        message = preprocess_message(message)
        prediction = model.predict([message])
        return prediction[0]
    except Exception as e:
        print(f"Erreur lors de la prédiction du spam : {e}")
        return -1  # -1 pour signaler une erreur