from tests.config import test_client, db_session, engine_session
from schemas.book import BookIn
from schemas.author import AuthorIn


class TestBook:
    def setup_class(self):
        self.valid_book = BookIn(
            name="Book",
            description="Book desc",
            amount=5,
            author_id=1,
        )
        self.valid_book_updated = BookIn(
            name="Book updated",
            description="Book updated desc",
            amount=3,
            author_id=1,
        )
        self.valid_author = AuthorIn(
            name="Author",
            second_name="Author sec"
        )

    def test_book_create(self, test_client):
        test_client.post(
            "/authors",
            json=self.valid_author.model_dump(),
        )
        response = test_client.post(
            "/books",
            json=self.valid_book.model_dump(),
        )
        book = response.json()
        assert response.status_code == 200
        assert book == {
            "id": 1,
            **self.valid_book.model_dump(exclude={"author_id"}),
            "author": {
                "id": 1,
                **self.valid_author.model_dump()
            }
        }

    def test_book_get(self, test_client):
        response = test_client.get(
            "/books/1"
        )
        book = response.json()
        assert response.status_code == 200
        assert book == {
            "id": 1,
            **self.valid_book.model_dump(exclude={"author_id"}),
            "author": {
                "id": 1,
                **self.valid_author.model_dump()
            }
        }

    def test_book_list(self, test_client):
        response = test_client.get(
            "/books"
        )
        book = response.json()
        assert response.status_code == 200
        assert len(book) == 1

    def test_book_update(self, test_client):
        response = test_client.put(
            "/books/1",
            json=self.valid_book_updated.model_dump(),
        )
        book = response.json()
        assert response.status_code == 200
        assert book == {
            "id": 1,
            **self.valid_book_updated.model_dump(exclude={"author_id"}),
            "author": {
                "id": 1,
                **self.valid_author.model_dump()
            }
        }

    def test_book_delete(self, test_client):
        response = test_client.delete(
            "/books/1",
        )
        body = response.json()
        assert body["status"] == "ok"
        response = test_client.get(
            "/books"
        )
        existed_books = response.json()
        assert len(existed_books) == 0
