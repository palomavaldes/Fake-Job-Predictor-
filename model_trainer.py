import numpy as np
import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, classification_report, confusion_matrix # Not directly used for saving models, but kept for completeness
from imblearn.under_sampling import RandomUnderSampler
import pickle # For saving models

# NLTK Downloads
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')
    print("NLTK stopwords downloaded.")

# LOAD THE DATA AND PROCESS DATA
    data = pd.read_csv("DataSet.csv")

data.drop(['salary_range', 'telecommuting', 'has_company_logo', 'has_questions', 'in_balanced_dataset'], axis=1, inplace=True)
data.fillna(' ', inplace=True)

# Create independent and dependent features
columns = data.columns.tolist()
columns = [c for c in columns if c not in ["fraudulent"]]
target = "fraudulent"
state = np.random.RandomState(42)
X = data[columns]
Y = data["fraudulent"]

# Handle Imbalanced Data
under_sampler = RandomUnderSampler(random_state=42) 
X_res, Y_res = under_sampler.fit_resample(X, Y)

df1 = pd.DataFrame(X_res, columns=X.columns) # Preserve column names
df3 = pd.DataFrame(Y_res, columns=[target]) # Preserve target column name

result = pd.concat([df1, df3], axis=1, join='inner')
data = result

# COMBINE TEXT COLUMNS
data['text'] = data['title']+' '+data['location']+' '+data['company_profile']+' '+data['description']+' '+data['requirements']+' '+data['benefits']+' '+data['industry']

# Drop original text columns
text_cols_to_drop = ['title', 'location', 'department', 'company_profile', 'description',
                     'requirements', 'benefits', 'required_experience', 'required_education',
                     'industry', 'function', 'country', 'employment_type']
data.drop(columns=text_cols_to_drop, inplace=True, errors='ignore') # Use errors='ignore' in case some cols were already dropped

# REMOVE HTML TAGS
def remove_html_tags(text):
    """Removes HTML tags from text."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(text)) # Ensure text is string

data['text'] = data['text'].apply(remove_html_tags)
data['text'] = data['text'].apply(lambda x: x.lower())

stop_words = set(stopwords.words("english"))
data['text'] = data['text'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in (stop_words)])) # Ensure x is string

# TRAIN-TEST SETS
X_train, X_test, Y_train, Y_test = train_test_split(data.text, data.fraudulent, test_size=0.3, random_state=42) # Added random_state for reproducibility

# VECTORIZATION OF DATA
vect = CountVectorizer()
vect.fit(X_train) # Fit only on training data
X_train_dtm = vect.transform(X_train)
X_test_dtm = vect.transform(X_test)

# DECISION TREE TRAINING
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train_dtm, Y_train)

# EVALUATE MODEL
Y_pred_class = dt.predict(X_test_dtm)
print("Decision Tree Accuracy:", accuracy_score(Y_test, Y_pred_class))
print("\nClassification Report:\n", classification_report(Y_test, Y_pred_class))
print("\nConfusion Matrix:\n", confusion_matrix(Y_test, Y_pred_class))

# SAVE MODEL
try:
    with open('count_vectorizer.pkl', 'wb') as f:
        pickle.dump(vect, f)
    print("count_vectorizer.pkl saved successfully!")

    with open('decision_tree_model.pkl', 'wb') as f:
        pickle.dump(dt, f)
    print("decision_tree_model.pkl saved successfully!")
except Exception as e:
    print(f"Error saving models: {e}")
