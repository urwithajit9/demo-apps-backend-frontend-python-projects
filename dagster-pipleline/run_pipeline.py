def run_pipeline():
    url = "https://example.com/articles"

    # Step 1: Scrape data
    data = scrape_data(url)

    # Step 2: Clean data
    cleaned_data = clean_data(data)

    # Step 3: Save cleaned data to a CSV
    save_data_to_csv(cleaned_data, "scraped_articles.csv")

if __name__ == "__main__":
    run_pipeline()
s
