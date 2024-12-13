import json

from schemas.author import AuthorIn
from schemas.book import BookIn
from schemas.borrow import BorrowIn
from tests.config import test_client, db_session, engine_session


class TestBorrow:
    def setup_class(self):
        self.valid_borrow = BorrowIn(
            book_id=1,
            reader_name="Reader",
            issue_date="2024-12-12",
        )
        self.valid_borrow_updated = BorrowIn(
            **self.valid_borrow.model_dump(exclude={"return_date"}),
            return_date="2024-12-12",
        )
        self.valid_author = AuthorIn(
            name="Author",
            second_name="Author sec",
        )
        self.valid_book = BookIn(
            name="Book",
            description="Book desc",
            amount=5,
            author_id=1,
        )

    def test_borrow_create(self, test_client):
        test_client.post(
            "/authors",
            json=self.valid_author.model_dump(),
        )
        test_client.post(
            "/books",
            json=self.valid_book.model_dump(),
        )
        borrow_json = json.loads(self.valid_borrow.model_dump_json())
        response = test_client.post(
            "/borrows",
            json=borrow_json,
        )
        assert response.status_code == 200
        borrow = response.json()
        assert borrow == {
            "id": 1,
            **json.loads(self.valid_borrow.model_dump_json(exclude={"book_id"})),
            "book": {
                "id": 1,
                **self.valid_book.model_dump(exclude={"author_id", "amount"}),
                "amount": self.valid_book.amount - 1,
                "author": {
                    "id": 1,
                    **self.valid_author.model_dump(),
                },
            }
        }

    def test_borrow_get(self, test_client):
        response = test_client.get(
            "/borrows/1",
        )
        assert response.status_code == 200
        borrow = response.json()
        assert borrow == {
            "id": 1,
            **json.loads(self.valid_borrow.model_dump_json(exclude={"book_id"})),
            "book": {
                "id": 1,
                **self.valid_book.model_dump(exclude={"author_id", "amount"}),
                "amount": self.valid_book.amount - 1,
                "author": {
                    "id": 1,
                    **self.valid_author.model_dump(),
                },
            }
        }

    def test_borrow_list(self, test_client):
        response = test_client.get(
            "/borrows"
        )
        assert response.status_code == 200
        borrows = response.json()
        assert len(borrows) == 1

    def test_borrow_update(self, test_client):
        date = str(self.valid_borrow_updated.return_date)
        response = test_client.patch(
            "/borrows/1/return",
            params={"return_date": date},
        )

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

        response = test_client.get(
            "/books/1",
        )
        book = response.json()
        assert book["amount"] == self.valid_book.amount
