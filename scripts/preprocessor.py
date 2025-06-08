import pandas as pd
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename='preprocessing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_reviews(input_csv, output_csv):
    try:
        logging.info("📥 Loading dataset...")
        df = pd.read_csv(input_csv)

        original_count = len(df)
        logging.info(f"Total reviews loaded: {original_count}")

        # Drop duplicates
        df = df.drop_duplicates(subset=['review_text', 'rating', 'date'])
        cleaned_count = len(df)
        logging.info(f"Removed {original_count - cleaned_count} duplicate entries")

        # Ensure date format
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Drop rows with missing values (if any)
        df.dropna(inplace=True)
        logging.info(f"Final cleaned review count: {len(df)}")

        # Save cleaned CSV
        df.to_csv(output_csv, index=False)
        logging.info(f"✅ Cleaned data saved to {output_csv}")

    except Exception as e:
        logging.error(f"❌ Error during preprocessing: {e}")

if __name__ == "__main__":
    preprocess_reviews("Dashen_reviews_20250607_214115.csv", "cleaned_reviews.csv")
