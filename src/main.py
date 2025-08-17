import requests

URL = "https://openlibrary.org"

def fetch_books_by_author(name):
    url = f"{URL}/search.json?author={name}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["docs"]

print(fetch_books_by_author("atwood"))