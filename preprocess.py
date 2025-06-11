import pandas as pd

df = pd.read_csv('raw_reviews.csv')

# Drop duplicates and missing values
df.drop_duplicates(subset=['review', 'rating', 'date'], inplace=True)
df.dropna(inplace=True)

# Normalize date
df['date'] = pd.to_datetime(df['date']).dt.date

# Save clean dataset
df.to_csv('clean_reviews.csv', index=False)
print("✅ Cleaned reviews saved to clean_reviews.csv")
