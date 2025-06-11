# Bank-Review-Analytics

# Google Play Store Reviews – Ethiopian Bank Apps

## Overview
This project scrapes and preprocesses user reviews from Google Play Store for three major Ethiopian banks.

### Targeted Apps
- CBE (Commercial Bank of Ethiopia): `com.combanketh.mobilebanking`
- BOA (Bank of Abyssinia): `com.boa.boaMobileBanking`
- Dashen Bank: `com.dashen.dashensuperapp`

## Methodology

### Scraping
Used `google-play-scraper` to fetch:
- Review content
- Ratings
- Review dates

Collected **400+ reviews per bank**.

### Preprocessing
- Removed duplicates and null entries
- Normalized date format to `YYYY-MM-DD`
- Output saved to `clean_reviews.csv`

## Files
- `play_store_scraper.py` – Scrapes 1200+ reviews from Google Play
- `preprocess.py` – Cleans and formats the data
- `requirements.txt` – Required Python packages
- `raw_reviews.csv` – Raw scraped data
- `clean_reviews.csv` – Preprocessed data

## Usage
```bash
pip install -r requirements.txt
python play_store_scraper.py
python preprocess.py
