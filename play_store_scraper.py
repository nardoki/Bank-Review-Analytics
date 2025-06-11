from google_play_scraper import reviews
import pandas as pd
import time

def fetch_reviews(app_id, bank_name, max_reviews=400):
    all_reviews = []
    continuation_token = None

    while len(all_reviews) < max_reviews:
        result, continuation_token = reviews(
            app_id,
            count=200,
            lang='en',
            country='us',
            continuation_token=continuation_token
        )
        all_reviews.extend(result)
        if continuation_token is None:
            break
        time.sleep(1)  # Polite delay to avoid request blocking

    df = pd.DataFrame(all_reviews)
    df['bank'] = bank_name
    df['source'] = 'Google Play Store'
    return df[['content', 'score', 'at', 'bank', 'source']].rename(
        columns={'content': 'review', 'score': 'rating', 'at': 'date'}
    )

# Bank apps and their IDs
apps = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp'
}

# Fetch and combine all reviews
all_dfs = []
for bank, app_id in apps.items():
    print(f"📥 Fetching reviews for {bank}...")
    df = fetch_reviews(app_id, bank)
    print(f"✅ Collected {len(df)} reviews for {bank}")
    all_dfs.append(df)

combined_df = pd.concat(all_dfs, ignore_index=True)
combined_df.to_csv('raw_reviews.csv', index=False)
print(f"\n📁 Saved total {len(combined_df)} reviews to raw_reviews.csv")
