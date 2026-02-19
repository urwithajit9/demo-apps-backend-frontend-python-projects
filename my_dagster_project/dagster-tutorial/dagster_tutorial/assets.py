import pandas as pd
import requests

from dagster import Output, asset

@asset
def hackernews_top_story_ids():
   """
   Get top stories from the HackerNews top stories endpoint.
   API Docs: https://github.com/HackerNews/API#new-top-and-best-stories
   """
   top_story_ids = requests.get(
       "https://hacker-news.firebaseio.com/v0/topstories.json"
   ).json()
   return top_story_ids[:10]

### asset dependencies can be inferred from parameter names
@asset
def hackernews_top_stories(context, hackernews_top_story_ids):
   """Get items based on story ids from the HackerNews items endpoint"""
   results = []
   for item_id in hackernews_top_story_ids:
       item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").json()
       results.append({item['title'],item['by'],item['url']})

   df = pd.DataFrame(results)

   context.log.info(df)

   return Output(value=df)

