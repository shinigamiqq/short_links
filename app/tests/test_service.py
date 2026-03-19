def test_cache_hit(monkeypatch):
    from app.services.link_service import get_original_url

    class FakeRedis:
        def get(self, key):
            return "cached_url"

    monkeypatch.setattr("app.services.link_service.redis_client", FakeRedis())

    result = get_original_url(None, "abc")

    assert result == "cached_url"


def test_increment_click(db):
    from app.services.link_service import create_link, increment_click

    link = create_link(db, "https://google.com", "click")

    increment_click(db, "click")

    assert link.clicks == 1
