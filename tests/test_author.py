from schemas.author import AuthorIn
from tests.config import test_client, db_session, engine_session


class TestAuthor:
    def setup_class(self):
        self.valid_author = AuthorIn(
            name="Author",
            second_name="Authorsec"
        )
        self.valid_author_updated = AuthorIn(
            name="Author",
            second_name="Authorsecup"
        )

    def test_author_create(self, test_client):
        response = test_client.post(
            "/authors",
            json=self.valid_author.model_dump()
        )
        author = response.json()
        assert response.status_code == 200
        assert author['id'] == 1
        assert author['name'] == self.valid_author.name
        assert author['second_name'] == self.valid_author.second_name

    def test_author_list(self, test_client):
        response = test_client.get(
            "/authors",
        )
        authors = response.json()
        assert response.status_code == 200
        assert len(authors) == 1

    def test_author_update(self, test_client):
        response = test_client.put(
            "/authors/1",
            json=self.valid_author_updated.model_dump()
        )
        author = response.json()
        assert response.status_code == 200
        assert author['id'] == 1
        assert author['name'] == self.valid_author_updated.name
        assert author['second_name'] == self.valid_author_updated.second_name

    def test_author_get(self, test_client):
        response = test_client.get(
            "/authors/1",
        )
        author = response.json()
        assert response.status_code == 200
        assert author['id'] == 1
        assert author['name'] == self.valid_author_updated.name
        assert author['second_name'] == self.valid_author_updated.second_name

    def test_author_delete(self, test_client):
        response = test_client.delete(
            "/authors/1",
        )
        body = response.json()
        assert body["status"] == "ok"
        response = test_client.get(
            "/authors"
        )
        existed_authors = response.json()
        assert len(existed_authors) == 0
