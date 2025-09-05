from src.utils import fetch_books_by_author, update_book_list, fetch_book_subjects, fetch_isbn_and_publisher_data, get_edition_key
import pytest
from unittest.mock import patch, Mock
import requests


@pytest.fixture
def mock_get_request():
    """Creates a test response body."""
    with patch("requests.get") as mock_get:
        response = Mock()
        response.json.return_value = {
            "numFound": 2428,
            "start": 0,
            "numFoundExact": True,
            "num_found": 2428,
            "documentation_url": "https://openlibrary.org/dev/docs/api/search",
            "q": "",
            "offset": None,
            "docs": [
                {
                    "author_key": ["OL52922A"],
                    "author_name": ["Margaret Atwood"],
                    "cover_edition_key": "OL2769393M",
                    "cover_i": 8231851,
                    "ebook_access": "borrowable",
                    "edition_count": 147,
                    "first_publish_year": 1985,
                    "has_fulltext": True,
                    "ia": [
                        "handmaidstale0000atwo_n4n6",
                        "handmaidstale2006atwo",
                        "handmaidstale00atwo_2"
                    ],
                    "ia_collection_s": "goffstownlibrary",
                    "key": "/works/OL675783W",
                    "language": [
                        "rum",
                        "eng",
                        "fin"
                    ],
                    "lending_edition_s": "OL38231252M",
                    "lending_identifier_s": "rasskazsluzhanki0000atwo_y8j3",
                    "public_scan_b": False,
                    "title": "The Handmaid's Tale"
                },
                {
                    "author_key": ["OL52922A"],
                    "author_name": ["Margaret Atwood"],
                    "cover_edition_key": "OL18632021M",
                    "cover_i": 11041760,
                    "ebook_access": "borrowable",
                    "edition_count": 89,
                    "first_publish_year": 2000,
                    "has_fulltext": True,
                    "ia": [
                        "letueuraveugle0000atwo",
                        "letueuraveuglero0000atwo",
                        "blindassassin0000atwo_j4u3",
                        "blindassassin0000atwo_u6w1"
                    ],
                    "ia_collection_s": "inlibrary",
                    "key": "/works/OL675698W",
                    "language": [
                        "heb",
                        "ben",
                        "eng"
                    ],
                    "lending_edition_s": "OL37790601M",
                    "lending_identifier_s": "letueuraveugle0000atwo",
                    "public_scan_b": False,
                    "title": "The Blind Assassin"
                }
            ]
        }
        mock_get.return_value = response
        yield mock_get


class TestFetchBooksByAuthor:
    """Tests for the book fetching function."""

    def test_returns_list_of_dicts(self, mock_get_request):
        """Checks that a list of dictionaries is returned."""
        result = fetch_books_by_author("name", "url")
        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)
    
    def test_returns_correct_data(self, mock_get_request):
        """Checks that correct data is returned."""
        result = fetch_books_by_author("name", "url")

        assert len(result) == 2
        assert result[0]["title"] == "The Handmaid's Tale"
        assert result[1]["title"] == "The Blind Assassin"
        
        for item in result:
            assert list(item.keys()) == [
                "author_key",
                "author_name",
                "cover_edition_key",
                "cover_i",
                "ebook_access",
                "edition_count",
                "first_publish_year",
                "has_fulltext",
                "ia",
                "ia_collection_s",
                "key",
                "language",
                "lending_edition_s",
                "lending_identifier_s",
                "public_scan_b",
                "title"
            ]
        
            assert isinstance(item["author_key"], list)
            assert isinstance(item["edition_count"], int)
            assert isinstance(item["has_fulltext"], bool)
            assert item["author_name"] == ['Margaret Atwood']

    def test_raise_for_status_called(self, mock_get_request):
        """Checks that status check is performed."""
        fetch_books_by_author("name", "url")
        mock_get_request.return_value.raise_for_status.assert_called_once()
    
    @pytest.mark.parametrize(
        "side_effect,expected_exception", [
            (requests.exceptions.HTTPError("404 Client Error"), requests.exceptions.HTTPError),
            (requests.exceptions.ConnectionError("Failed to connect"), requests.exceptions.ConnectionError),
            (requests.exceptions.Timeout("Request timed out"), requests.exceptions.Timeout),
        ]
    )
    def test_correct_errors_raised(self, side_effect, expected_exception):
        """Checks that errors are raised."""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = side_effect
            mock_get.return_value = mock_response

            with pytest.raises(expected_exception):
                fetch_books_by_author("name", "url")


@pytest.fixture
def dummy_book_list():
    """Creates a dummy book list."""
    dummy_list = [
        {
            "author_key": ["OL52922A"],
            "author_name": ["Margaret Atwood"],
            "cover_edition_key": "OL2769393M",
            "cover_i": 8231851,
            "ebook_access": "borrowable",
            "edition_count": 147,
            "first_publish_year": 1985,
            "has_fulltext": True,
            "ia": [
                "handmaidstale0000atwo_n4n6",
                "handmaidstale2006atwo",
                "handmaidstale00atwo_2"
            ],
            "ia_collection_s": "goffstownlibrary",
            "key": "/works/OL675783W",
            "language": [
                "rum",
                "eng",
                "fin"
            ],
            "lending_edition_s": "OL38231252M",
            "lending_identifier_s": "rasskazsluzhanki0000atwo_y8j3",
            "public_scan_b": False,
            "title": "The Handmaid's Tale"
        },
        {
            "author_key": ["OL52922A"],
            "author_name": ["Margaret Atwood"],
            "cover_edition_key": "OL18632021M",
            "cover_i": 11041760,
            "ebook_access": "borrowable",
            "edition_count": 89,
            "first_publish_year": 2000,
            "has_fulltext": True,
            "ia": [
                "letueuraveugle0000atwo",
                "letueuraveuglero0000atwo",
                "blindassassin0000atwo_j4u3",
                "blindassassin0000atwo_u6w1"
            ],
            "ia_collection_s": "inlibrary",
            "key": "/works/OL675698W",
            "language": [
                "heb",
                "ben",
                "eng"
            ],
            "lending_edition_s": "OL37790601M",
            "lending_identifier_s": "letueuraveugle0000atwo",
            "public_scan_b": False,
            "title": "The Blind Assassin"
        }
    ]
    yield dummy_list


class TestUpdateBookList:
    """Tests for the update_book_list function."""

    def test_returns_new_list(self, dummy_book_list):
        """Checks that a new list is returned."""
        result = update_book_list(dummy_book_list)

        assert result is not dummy_book_list


    def test_returns_correctly_updated_data(self, dummy_book_list):
        """Checks that correct data is returned."""
        result = update_book_list(dummy_book_list)

        assert len(result) == 2

        for book in result:
            assert list(book.keys()) == [
                "id",
                "title",
                "author_name",
                "first_publish_year",
                "edition_count",
                "language"
            ]
        
        assert result[0]["id"] == "/works/OL675783W"
        assert result[0]["title"] == "The Handmaid's Tale"
        assert result[0]["author_name"] == ["Margaret Atwood"]
        assert result[0]["first_publish_year"] == 1985
        assert result[0]["edition_count"] == 147
        assert result[0]["language"] == [
            "rum",
            "eng",
            "fin"
        ]
    
    def test_updates_with_empty_lists_if_keys_missing(self, dummy_book_list):
        """Checks that empty lists are included if keys missing."""
        keys_to_remove = ["author_name", "first_publish_year", "language"]

        for key in keys_to_remove:
            dummy_book_list[0].pop(key)
        
        result = update_book_list(dummy_book_list)

        assert list(result[0].keys()) == [
                "id",
                "title",
                "author_name",
                "first_publish_year",
                "edition_count",
                "language"
            ]
        
        assert result[0]["author_name"] == []
        assert result[0]["first_publish_year"] == []
        assert result[0]["language"] == []
    
    def test_empty_book_list_returns_empty_list(self):
        """Checks empty list is returned if book list is empty."""
        result = update_book_list([])

        assert result == []


@pytest.fixture
def mock_subject_request():
    """Creates a subjects response body."""
    with patch("requests.get") as mock_get:
        response = Mock()
        response.json.return_value = {
            "covers": [
                4860886, 
                4860885
            ], 
            "key": "/works/OL675737W", 
            "authors": [
                {
                    "author": {
                        "key": "/authors/OL52922A"
                    }, 
                    "type": {
                        "key": "/type/author_role"
                    }
                }
            ], 
            "title": "The Penelopiad", 
            "subjects": [
                "Penelope (Greek mythology)", 
                "Odysseus (Greek mythology)", 
                "Fiction"
            ], 
            "type": {
                "key": "/type/work"
            }, 
            "description": "Homer's Odyssey is not the only version of the story.",
            "latest_revision": 18, 
            "revision": 18, 
            "created": {
                "type": "/type/datetime", 
                "value": "2009-12-09T01:02:43.882811"
            }, 
            "last_modified": {
                "type": "/type/datetime", 
                "value": "2024-09-23T14:42:30.367966"
            }
        }
        mock_get.return_value = response
        yield mock_get


class TestFetchBookSubjects:
    """Tests for the fetch_book_subjects function."""

    def test_raise_for_status_called(self, mock_subject_request):
        """Checks that status check is performed."""
        fetch_book_subjects("/works/OL675783W", "url")
        mock_subject_request.return_value.raise_for_status.assert_called_once()
    
    @pytest.mark.parametrize(
        "side_effect,expected_exception", [
            (requests.exceptions.HTTPError("404 Client Error"), requests.exceptions.HTTPError),
            (requests.exceptions.ConnectionError("Failed to connect"), requests.exceptions.ConnectionError),
            (requests.exceptions.Timeout("Request timed out"), requests.exceptions.Timeout),
        ]
    )
    def test_correct_errors_raised(self, side_effect, expected_exception):
        """Checks that errors are raised."""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = side_effect
            mock_get.return_value = mock_response

            with pytest.raises(expected_exception):
                fetch_book_subjects("/works/OL675783W", "url")
    
    def test_returns_correct_data(self, mock_subject_request):
        """Checks correct data is returned."""
        result = fetch_book_subjects("/works/OL675783W", "url")
        assert isinstance(result, dict)
        assert list(result.keys()) == ["subjects"]
        assert result["subjects"] == [
            "Penelope (Greek mythology)",
            "Odysseus (Greek mythology)",
            "Fiction"
        ]


@pytest.fixture
def mock_edition_request():
    """Creates an edition key response body."""
    with patch("requests.get") as mock_get:
        response = Mock()
        response.json.return_value = {
            "description": {
                "type": "/type/text", 
                "value": "The Handmaid's Tale is a radical departure for Margaret Atwood."
            }, 
            "identifiers": {
                "librarything": ["1667444"], 
                "alibris_id": ["9780771008139"]
            }, 
            "title": "The Handmaid's Tale",
            "authors": [{"key": "/authors/OL52922A"}], 
            "publish_date": "1985", 
            "publishers": [
                "McClelland & Stewart",
                "McClelland and Stewart"
            ], 
            "covers": [8231851], 
            "physical_format": "Hardcover", 
            "publish_places": ["Toronto, Canada"], 
            "uri_descriptions": [
                "Contributor biographical information", 
                "Publisher description"
            ], 
            "pagination": "324 p. ;", 
            "source_records": [
                "promise:bwb_daily_pallets_2022-09-01:W7-CMU-382",
                "marc:marc_records_scriblio_net/part18.dat:195613967:911"
            ], 
            "url": [
                "http://www.loc.gov/catdir/bios/random056/86129018.html", 
                "http://www.loc.gov/catdir/description/random0411/86129018.html"
            ], 
            "languages": [{"key": "/languages/eng"}], 
            "subjects": [
                "Man-woman relationships -- Fiction", 
                "Misogyny -- Fiction", "Women -- Fiction"
            ], 
            "publish_country": "onc", 
            "copyright_date": "1985", 
            "by_statement": "Margaret Atwood.", 
            "type": {"key": "/type/edition"}, 
            "uris": [
                "http://www.loc.gov/catdir/bios/random056/86129018.html", 
                "http://www.loc.gov/catdir/description/random0411/86129018.html"
            ], 
            "ocaid": "handmaidstale00marg", 
            "isbn_10": ["0771008139"], 
            "isbn_13": ["9780771008139"], 
            "lccn": ["86129018"], 
            "dewey_decimal_class": ["813/.54"], 
            "lc_classifications": [
                "PR9199.3.A8 H3 1985", 
                "PR9501 .T86N35 1985"
            ], 
            "local_id": ["urn:bwbsku:W7-CMU-382", "urn:bwbsku:P7-EDL-594"], 
            "key": "/books/OL2769393M", 
            "number_of_pages": 324, 
            "works": [{"key": "/works/OL675783W"}], 
            "oclc_numbers": ["12825460"], 
            "latest_revision": 28, 
            "revision": 28, 
            "created": {"type": "/type/datetime", "value": "2008-04-01T03:28:50.625462"}, 
            "last_modified": {
                "type": "/type/datetime", 
                "value": "2024-07-21T21:40:12.749893"
            }
        }
        mock_get.return_value = response
        yield mock_get


class TestFetchISBNandPublisherData:
    """Tests for the fetch_isbn_and_publisher_data function."""

    def test_raise_for_status_called(self, mock_edition_request):
        """Checks that status check is performed."""
        fetch_isbn_and_publisher_data("OL2769393M", "url")
        mock_edition_request.return_value.raise_for_status.assert_called_once()
    
    @pytest.mark.parametrize(
        "side_effect,expected_exception", [
            (requests.exceptions.HTTPError("404 Client Error"), requests.exceptions.HTTPError),
            (requests.exceptions.ConnectionError("Failed to connect"), requests.exceptions.ConnectionError),
            (requests.exceptions.Timeout("Request timed out"), requests.exceptions.Timeout),
        ]
    )
    def test_correct_errors_raised(self, side_effect, expected_exception):
        """Checks that errors are raised."""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = side_effect
            mock_get.return_value = mock_response

            with pytest.raises(expected_exception):
                fetch_isbn_and_publisher_data("OL2769393M", "url")
    
    def test_returns_correct_data(self, mock_edition_request):
        """Checks that correct data is returned."""
        result = fetch_isbn_and_publisher_data("OL2769393M", "url")
        assert list(result.keys()) == ["publisher", "isbn"]
        assert result["publisher"] == [
            "McClelland & Stewart",
            "McClelland and Stewart"
        ]
        assert result["isbn"] == {
            "isbn_10": ["0771008139"], 
            "isbn_13": ["9780771008139"]
        } 

    def test_returns_empty_lists_for_missing_isbn_numbers(self, mock_edition_request):
        """Checks empty list is returned in place of missing ISBN."""

        keys_to_remove = ["isbn_10", "isbn_13"]
        for key in keys_to_remove:
            mock_edition_request.return_value.json.return_value.pop(key)

        result = fetch_isbn_and_publisher_data("OL2769393M", "url")

        assert list(result.keys()) == ["publisher", "isbn"]
        assert result["publisher"] == [
            "McClelland & Stewart",
            "McClelland and Stewart"
        ]
        assert result["isbn"] == {
            "isbn_10": [], 
            "isbn_13": []
        } 

@pytest.fixture
def book_data_example():
    """A dummy book dictionary with a cover edition key."""
    book = {
        "author_key": [
            "OL52922A"
        ],
        "author_name": [
            "Margaret Atwood"
        ],
        "cover_edition_key": "OL18632021M",
        "title": "The Blind Assassin"
    }
    yield book

class TestGetEditionKey:
    """Tests for the get_edition_key function."""

    def test_returns_cover_edition_key(self, book_data_example):
        """Checks that cover_edition_key is returned."""
        result = get_edition_key(book_data_example)

        assert result == "OL18632021M"
    
    def test_returns_lending_edition_key(self, book_data_example):
        """Checks that lending_edition key is returned."""
        book_data_example.pop("cover_edition_key")
        book_data_example["lending_edition_s"] = "OL7038266M"

        result = get_edition_key(book_data_example)

        assert result == "OL7038266M"
    
    def test_returns_none_if_no_edition_key(self, book_data_example):
        """Checks None is returned if no edition key."""
        book_data_example.pop("cover_edition_key")

        result = get_edition_key(book_data_example)

        assert result == None


        
