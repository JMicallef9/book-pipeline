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

def update_book_data(book_data):
    """
    Simplifies and updates book data.

    Args:
        book_data (dict): A dictionary containing information about a book.
    
    Returns:
        dict: A streamlined set of data with updated key-value pairs.
    """
    book_dict = {}

    if not book_data:
        return book_dict

    book_dict["id"] = book_data["key"]
    book_dict["title"] = book_data["title"]
    book_dict["author_name"] = book_data.get("author_name", [])
    book_dict["first_publish_year"] = book_data.get("first_publish_year", [])
    book_dict["edition_count"] = book_data["edition_count"]
    book_dict["language"] = book_data.get("language", [])
    
    return book_dict

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

def merge_dicts(*dicts):
    """
    Merges multiple dictionaries into single dictionary.

    Args:
        dictionaries (dict): Two or more dictionaries.
    
    Returns:
        dict: A merged dictionary.
    """
    new_dict = {}

    for d in dicts:
        for key, value in d.items():
            if key not in new_dict:
                new_dict[key] = value
            else:
                if not isinstance(new_dict[key], list) and value is not new_dict[key]:
                    new_dict[key] = [new_dict[key]]
                    new_dict[key].append(value)
    
    return new_dict

def generate_book_data(author, url):
    """
    Retrieves and formats data for an author's books.

    Args:
        name (str): The name of an author.
        url (str): An openlibrary URL.
    
    Returns:
        list: A list of pipeline-ready data about the author's books. 
    """
    book_list = fetch_books_by_author(author, url)

    new_book_list = []

    for book in book_list:

        edition_key = get_edition_key(book)
    
        updated_book = update_book_data(book)

        subjects = fetch_book_subjects(updated_book["id"], url)

        isbn_data = fetch_isbn_and_publisher_data(edition_key, url)

        new_dict = merge_dicts(updated_book, subjects, isbn_data)

        new_book_list.append(new_dict)
    
    return new_book_list