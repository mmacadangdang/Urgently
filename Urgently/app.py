# ------------------------------------------------------------------------------
# Import library dependencies
import pandas as pd
import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from nltk.stem import WordNetLemmatizer
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

# Import local file dependencies
import api_config

# ------------------------------------------------------------------------------
# Boilerplate for creating the app via Flask
app = Flask(__name__)

# ------------------------------------------------------------------------------
# Homepage/index route
@app.route("/")
def index():
    """Homepage requested."""

    return render_template("index.html")

# ------------------------------------------------------------------------------
# Data route for sales
@app.route("/calculator/<input>")
# Accepts a string
def calculator(input):
    """Calculator requested."""
    print(f"Calculator requests.  Input string is: \n{input}")

    # Create a list of filler data using data from the CSV of manually categorized data, and add the user's input to it
    filler_df = pd.read_csv('Working CSV.csv')
    data = filler_df['public_description'].tolist()
    data.append(input)

    # ------------------------------------------------------------------------------
    # Data pre-processing
    documents = []

    for sen in range(0, len(data)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(data[sen]))

        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Converting to Lowercase
        document = document.lower()
        documents.append(document)

    # ------------------------------------------------------------------------------
    # Encoding

    # Use Bag of Words to to encode text
    print("Beginning Bag of Words encoding")
    vectorizer = CountVectorizer(max_features=1500, min_df=1, max_df=3, stop_words=stopwords.words('english'))
    documents = vectorizer.fit_transform(documents).toarray()
    print("Bag of Words encoding complete")

    # Transform the Bag Of Words array to calculate TF-IDF
    print("Beginning TF-IDF calculation")
    tfidfconverter = TfidfTransformer()
    documents = tfidfconverter.fit_transform(documents).toarray()
    print("TF-IDF calculation complete")
    print(documents)

    # ------------------------------------------------------------------------------
    # Load the existing model
    print("Loading the model")
    with open('text_classifier', 'rb') as training_model:
        model = pickle.load(training_model)
    print("Model loaded")

    # ------------------------------------------------------------------------------
    # Use the model to calculate urgency
    print("Making prediction calculation")
    urgentValue = model.predict(documents)
    print(f"\n**Urgency calculated** \nResult array: {urgentValue}")

    # Extract the last element in the array.  That's the prediction for the user-entered data
    urgentSelection = len(data)-1
    print(f"Final array value for prediction: {urgentSelection}")
    urgentValue = urgentValue[urgentSelection]
    print(f"urgentValue: {urgentValue}")

    # Determine the urgency image that should be shown based don the prediction
    if urgentValue == 'yes':
        urgencyImage = {'URL': 'static/img/urgent.png'}
    else:
        urgencyImage = {'URL': 'static/img/not_urgent.png'}
        if ("gun" in input) or ("intersection" in input) or ("pothole" and "tire" in input):
            print(f"**Likely mis-categorization**\n{input}\n---------------------")

    print(f"Dictionary that will be returned:\n {urgencyImage}")
    # Return the path to the resulting urgency image
    return jsonify(urgencyImage)
# ------------------------------------------------------------------------------
# Boilerplate for running the code as an app through Flask
if __name__ == "__main__":
    app.run()
# ------------------------------------------------------------------------------
