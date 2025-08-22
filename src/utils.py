import requests

def fetch_books_by_author(name, url):
    url = f"{url}/search.json?author={name}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["docs"]

def update_book_list(book_list):
    book_details = []
    for book in book_list:
        book_dict = {}
        book_dict["id"] = book["key"]
        book_dict["title"] = book["title"]
        book_dict["author_name"] = book.get(["author_name"], [])
        book_dict["first_publish_year"] = book.get(["first_publish_year"], [])
        book_dict["edition_count"] = book["edition_count"]
        book_dict["language"] = book.get(["language"], [])
        book_details.append(book_dict)
    
    return book_details

def fetch_book_subjects(book_key, url):
    url = f"{url}{book_key}.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    book_dict = {}
    book_dict["subjects"] = data.get(["subjects"], [])
    return book_dict

def fetch_isbn_and_publisher_data(edition_key, url):
    url = f"{url}/books/{edition_key}.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    book_dict = {}
    book_dict["publisher"] = data["publishers"]
    book_dict["isbn"] = {
        ["isbn_10"]: data.get(["isbn_10"], []),
        ["isbn_13"]: data.get(["isbn_13"], [])
    }
    return book_dict

def get_cover_edition_key(book):
    return book.get("cover_edition_key") or (book.get("edition_key", [None])[0])