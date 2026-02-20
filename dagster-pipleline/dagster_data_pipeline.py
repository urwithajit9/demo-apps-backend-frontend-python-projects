from dagster import op, job
import pandas as pd

@op
def scrape_data_op():
    url = "https://example.com/articles"
    data = scrape_data(url)
    return data

@op
def clean_data_op(data):
    cleaned_data = clean_data(data)
    return cleaned_data

@op
def save_data_op(cleaned_data):
    save_data_to_csv(cleaned_data, "articles.csv")

@job
def data_pipeline():
    raw_data = scrape_data_op()
    cleaned_data = clean_data_op(raw_data)
    save_data_op(cleaned_data)


#dagit -f pipeline.py
