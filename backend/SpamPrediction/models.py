from django.db import models
import joblib

class SpamDetector:
    def __init__(self):
        self.model = joblib.load("spam_sms_detector.pkl")  # Replace with correct path
        self.vectorizer = joblib.load("tfidf_vectorizer.pkl")  # Replace with correct path

    def predict(self, sms):
        new_sms_features = self.vectorizer.transform([sms])
        prediction = self.model.predict(new_sms_features)[0]
        if prediction == 1:
            return "spam"
        else:
            return "not spam"
