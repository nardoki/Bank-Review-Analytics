from google_play_scraper import Sort, reviews
import csv
from datetime import datetime
import schedule
import logging
import time

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_play_store_reviews():
    APP_ID = 'com.dashen.dashensuperapp'
    logging.info("🔄 Fetching reviews...")

    try:
        results, _ = reviews(
            APP_ID,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=5000,
            filter_score_with=None
        )

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'Dashen_reviews_{timestamp}.csv'

        # Write to CSV without using pandas
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['review_text', 'rating', 'date', 'bank_name', 'source'])
            writer.writeheader()

            for entry in results:
                writer.writerow({
                    'review_text': entry['content'],
                    'rating': entry['score'],
                    'date': entry['at'].strftime('%Y-%m-%d'),
                    'bank_name': 'Commercial Bank of Ethiopia',
                    'source': 'Google Play'
                })

        logging.info(f"✅ Saved {len(results)} reviews to {filename}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

# Different scheduling options (uncomment the one you want to use):
schedule.every().day.at("01:00").do(scrape_play_store_reviews)  # Daily at 1 AM
# schedule.every(6).hours.do(scrape_play_store_reviews)           # Every 6 hours
# schedule.every().monday.do(scrape_play_store_reviews)           # Every Monday
# schedule.every().hour.do(scrape_play_store_reviews)             # Every hour

while True:
    schedule.run_pending()
    time.sleep(1)