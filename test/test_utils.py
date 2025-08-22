from src.utils import fetch_books_by_author
import pytest
from unittest.mock import patch, Mock


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
        yield


class TestFetchBooksByAuthor:
    """Tests for the book fetching function."""

    def test_returns_list_of_dicts(self, mock_get_request):
        """Checks that a list of dictionaries is returned."""
        result = fetch_books_by_author("url", "name")
        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

        print(result)


