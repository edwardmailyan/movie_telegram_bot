import pandas as pd
import time
import requests


class NotionClient:
    def __init__(self, notion_token, db_id):
        self.headers = {
            "Authorization": "Bearer " + notion_token,
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json"
        }
        self.last_refresh_time = None
        self.db_id = db_id
        self.movies = self.get_movies()

    def get_pages(self, num_pages=None):
        url = f"https://api.notion.com/v1/databases/{self.db_id}/query"

        get_all = num_pages is None

        page_size = 100 if get_all else num_pages
        payload = {"page_size": 100,
                   "filter": {
                       "property": "Status",
                       "select": {
                           "equals": "new"
                       }
                   }
                   }
        response = requests.post(url, json=payload, headers=self.headers)

        data = response.json()
        results = data['results']

        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            response = requests.post(url, json=payload, headers=self.headers)
            data = response.json()
            results.extend(data["results"])

        results = pd.json_normalize(results)

        return results

    def get_movies(self):
        pages = self.get_pages()
        movies = pages[['properties.Title.title',
                        'properties.Status.select.name',
                        'properties.Rating.number']].rename(columns=lambda x: x.split('.')[1])
        movies['Title'] = movies['Title'].apply(lambda x: x[0]['text']['content'])
        self.last_refresh_time = time.monotonic()
        return movies

    def get_random_movies(self, n):
        if time.monotonic() - self.last_refresh_time > 1800:
            self.movies = self.get_movies()

        return self.movies.sample(n)['Title'].values
