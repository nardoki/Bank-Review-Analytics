# ======= 1. Import Libraries =======
import pandas as pd
from transformers import pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# ======= 2. Load Dataset =======
df = pd.read_csv("raw_reviews.csv")

# ======= 3. Run Sentiment Analysis =======
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    result = classifier(text[:512])[0]  # Truncate to 512 characters
    return result['label'], result['score']

df[['sentiment_label', 'sentiment_score']] = df['review'].astype(str).apply(lambda x: pd.Series(analyze_sentiment(x)))

# ======= 4. NLP Preprocessing (tokenize, stopword, lemmatize) =======
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

df['cleaned_review'] = df['review'].astype(str).apply(preprocess)

# ======= 5. TF-IDF Keyword Extraction =======
vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
X = vectorizer.fit_transform(df['cleaned_review'])

keywords = vectorizer.get_feature_names_out()
df_keywords = pd.DataFrame(X.toarray(), columns=keywords)

# ======= 6. Manual Theme Grouping =======
themes = {
    "Login Issues": ["login", "signin", "password", "access"],
    "Transaction Problems": ["transfer", "transaction", "delay", "fail", "slow"],
    "App UI/UX": ["design", "interface", "navigation", "layout", "easy", "hard"],
    "Customer Support": ["support", "help", "response", "service"],
    "Feature Request": ["feature", "add", "option", "include", "wish"]
}

def assign_theme(text):
    matched_themes = []
    for theme, keywords in themes.items():
        if any(word in text for word in keywords):
            matched_themes.append(theme)
    return ', '.join(matched_themes) if matched_themes else 'Other'

df['themes'] = df['cleaned_review'].apply(assign_theme)

# ======= 7. Save Final Output =======
df.to_csv("reviews_with_sentiment_and_themes.csv", index=False)
print("✅ Analysis complete. Output saved to 'reviews_with_sentiment_and_themes.csv'")

# Select and rename the columns you want in the final CSV
final_df = df[[
    'review',               # Original review text
    'rating',               # If you have it; add this if your df has a rating column
    'sentiment_label',      # Sentiment label: POSITIVE/NEGATIVE
    'sentiment_score',      # Sentiment confidence score
    'themes'                # Assigned theme(s)
]].copy()

# If 'rating' column is missing in your df, remove it from above list

# Save the clean table to CSV
final_df.to_csv("reviews_with_sentiment_and_themes.csv", index=False)

print("✅ Clean CSV saved to 'reviews_with_sentiment_and_themes.csv'")
