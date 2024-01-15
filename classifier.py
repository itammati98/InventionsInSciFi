# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 15:25:14 2024

@author: Matt
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Prepare the Data

# Load patent descriptions
patent_data = pd.read_csv(r'C:\Users\Matt\Desktop\DH_FinalProject\patent_training.csv', encoding='utf-8')

# Load mined paragraphs for training
mined_data = pd.read_csv(r'C:\Users\Matt\Desktop\DH_FinalProject\output\output_training.csv', encoding='utf-8')

# Load mined paragraphs from scifi
scifi_mined = pd.read_csv(r'C:\Users\Matt\Desktop\DH_FinalProject\output\outputauto.csv', encoding='utf-8')

# Step 2: Label the Data

patent_data['label'] = 'invention'
mined_data['label'] = 'book'

# Step 3: Combine and Shuffle Data

combined_data = pd.concat([patent_data, mined_data], ignore_index=True)
combined_data = combined_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Step 4: Text Vectorization

vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X = vectorizer.fit_transform(combined_data['text'].values.astype('U'))
y = combined_data['label']

# Step 5: Train a Classifier

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

classifier = LogisticRegression()
classifier.fit(X_train, y_train)

# Step 6: Evaluate the Model

y_pred = classifier.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)

print(f"Accuracy on validation set: {accuracy}")
print("Classification Report:")
print(classification_report(y_val, y_pred))

# Step 7: Classify Mined Paragraphs

mined_paragraphs = vectorizer.transform(scifi_mined['text'])
mined_predictions = classifier.predict(mined_paragraphs)

scifi_mined['prediction'] = mined_predictions

# Display the results
print("\nClassified Mined Paragraphs:")
print(scifi_mined[['text', 'prediction']])

results_csv_path = r'C:\Users\Matt\Desktop\DH_FinalProject\results_training.csv'
combined_data.to_csv(results_csv_path, index=False)
scifi_mined.to_csv(r'C:\Users\Matt\Desktop\DH_FinalProject\mined_results_scifi.csv', index=False)

print(f"\nResults saved to '{results_csv_path}' and 'path/to/mined_results.csv'.")
