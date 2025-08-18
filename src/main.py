import requests

URL = "https://openlibrary.org"

def fetch_books_by_author(name):
    url = f"{URL}/search.json?author={name}"
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
        book_dict["author_name"] = book["author_name"]
        book_dict["first_publish_year"] = book["first_publish_year"]
        book_dict["edition_count"] = book["edition_count"]
        book_dict["language"] = book["language"]
        book_details.append(book_dict)

def fetch_book_details(book_key):
    url = f"{URL}{book_key}.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    book_dict = {}
    book_dict["subjects"] = data["subjects"]




print(fetch_books_by_author("atwood"))


# {
# "id": "/works/OL82563W",
# "title": "The Hobbit",
# "author_name": ["J.R.R. Tolkien"],
# "first_publish_year": 1937,
# "edition_count": 300,
# "subjects": ["Fantasy", "Adventure", "Hobbits"],
# "language": ["eng"],
# "publisher": ["George Allen & Unwin", "Houghton Mifflin"],
# "isbn": ["9780007525492", "0261102214"]
# }

# /books/{edition_key}.json