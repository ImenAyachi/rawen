import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

# Chemins vers les datasets
sms_path = 'data/spam.csv'
email_path = 'data/emails.csv'

# Charger les jeux de données
sms_df = pd.read_csv(sms_path, encoding='latin-1')[['v1', 'v2']]
sms_df.columns = ['label', 'message']
sms_df['label'] = sms_df['label'].map({'ham': 0, 'spam': 1})

email_df = pd.read_csv(email_path)[['text', 'spam']]
email_df.columns = ['message', 'label']

# Combiner les datasets
combined_df = pd.concat([sms_df, email_df], ignore_index=True)

# Train model after preprocessing
def preprocess_message(message):
    """
    Amélioration du prétraitement du texte
    """
    # Code du prétraitement ici (voir la fonction ci-dessus)
    pass
# Créer pipeline d'entraînement
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

combined_df['message'] = combined_df['message'].astype(str)

# Entraîner le modèle
pipeline.fit(combined_df['message'], combined_df['label'])

# Sauvegarder le modèle
os.makedirs('model', exist_ok=True)
with open('model/spam.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

print("✅ Modèle entraîné et enregistré dans model/spam.pkl")
