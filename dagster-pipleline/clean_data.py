import re
import pandas as pd

def clean_data(data):
    cleaned_data = []

    for item in data:
        # Clean title (remove special characters)
        title_cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", item["title"]).strip().lower()

        # Convert date to datetime format
        date_cleaned = pd.to_datetime(item["date"], errors='coerce')

        # Append cleaned data to the list
        cleaned_data.append({
            "title": title_cleaned,
            "date": date_cleaned
        })

    # Remove entries with missing dates or duplicates
    df = pd.DataFrame(cleaned_data)
    df.dropna(subset=["date"], inplace=True)
    df.drop_duplicates(subset=["title"], inplace=True)

    return df
