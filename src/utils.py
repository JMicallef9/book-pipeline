import requests

def fetch_books_by_author(name, url):
    """
    Fetches a list of books from the openlibrary API.
    
    Args:
        name (str): The name of an author.
        url (str): An openlibrary URL.
    
    Returns:
        list: A list of dictionaries with information about the author's books. 
    """
    url = f"{url}/search.json?author={name}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["docs"]

def update_book_list(book_list):
    """
    Simplifies a list of books and updates relevant data.

    Args:
        book_list (list): A list of dictionaries containing information about books.
    
    Returns:
        list: A new list of books with updated key-value pairs.
    """
    book_details = []
    for book in book_list:
        book_dict = {}
        book_dict["id"] = book["key"]
        book_dict["title"] = book["title"]
        book_dict["author_name"] = book.get("author_name", [])
        book_dict["first_publish_year"] = book.get("first_publish_year", [])
        book_dict["edition_count"] = book["edition_count"]
        book_dict["language"] = book.get("language", [])
        book_details.append(book_dict)
    
    return book_details

def fetch_book_subjects(book_key, url):
    """
    Retrieves the list of subjects for a book.
    
    Args:
        url (str): The main openlibrary URL.
        book_key (str): The openlibrary key for a book.
    
    Returns:
        dict: A dictionary listing the book's subjects.
    """
    url = f"{url}{book_key}.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    book_dict = {}
    book_dict["subjects"] = data.get("subjects", [])
    return book_dict

def fetch_isbn_and_publisher_data(edition_key, url):
    """
    Retrieves a book's ISBN and publisher data.
    
    Args:
        edition_key (str): A book's edition key.
        url (str): An openlibrary URL.
    
    Returns:
        dict: The book's ISBN and publisher data.
    """
    url = f"{url}/books/{edition_key}.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    book_dict = {}
    book_dict["publisher"] = data["publishers"]
    book_dict["isbn"] = {
        "isbn_10": data.get("isbn_10", []),
        "isbn_13": data.get("isbn_13", [])
    }
    return book_dict

def get_edition_key(book):
    """
    Retrieves a book's edition key.

    Args:
        book (dict): A dictionary representing a book.

    Returns:
        str: The book's edition key.
    """
    return book.get("cover_edition_key") or (book.get("lending_edition_s"))

def merge_dicts(*dictionaries):
    """
    Merges multiple dictionaries into single dictionary.

    Args:
        dictionaries (dict): Two or more dictionaries.
    
    Returns:
        dict: A merged dictionary.
    """
    new_dict = {}

    for d in dictionaries:
        for key, value in d.items():
            if key not in new_dict:
                new_dict[key] = value
    
    return new_dict