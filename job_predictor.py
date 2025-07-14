import pickle
import re
import string
import nltk
from nltk.corpus import stopwords

# NLTK downloads (if havent already)
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')
    print("NLTK stopwords downloaded for job_predictor.")


# Load the trained CountVectorizer and Decision Tree Model
count_vectorizer = None
decision_tree_model = None

try:
    with open('count_vectorizer.pkl', 'rb') as f:
        count_vectorizer = pickle.load(f)
    with open('decision_tree_model.pkl', 'rb') as f:
        decision_tree_model = pickle.load(f)
    print("Models loaded successfully by job_predictor!")
except FileNotFoundError:
    print("Error: Model files not found. Please ensure 'count_vectorizer.pkl' and 'decision_tree_model.pkl' are in the correct directory.")
    print("Run 'python model_trainer.py' to generate these files.")
except Exception as e:
    print(f"An error occurred while loading models: {e}")


# Text Preprocessing Functions

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(text)) # Ensure text is string

def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    # 1. Remove HTML tags
    text = remove_html_tags(text)

    # 2. Convert to lowercase
    text = text.lower()

    # 3. Remove stopwords
    stop_words = set(stopwords.words("english"))
    text = ' '.join([word for word in text.split() if word not in (stop_words)])

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Prediction function

def predict_job_fraud(job_description: str) -> str:
    if count_vectorizer is None or decision_tree_model is None:
        return "Error: Model not loaded. Cannot make prediction."

    # 1. Preprocess the input text
    processed_text = preprocess_text(job_description)

    # 2. Vectorize the preprocessed text (input is list of strings)
    input_data_features = count_vectorizer.transform([processed_text])

    # 3. Make prediction
    prediction_array = decision_tree_model.predict(input_data_features)

    # 4. Interpret the prediction (t for fraud and f for real)
    if prediction_array[0] == 't':
        return "Fraudulent Job"
    else:
        return "Real Job"

