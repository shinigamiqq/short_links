def test_create_link(client):
    response = client.post("/links/shorten", json={
        "original_url": "https://google.com"
    })

    assert response.status_code == 200
    assert "short_url" in response.json()


def test_redirect(client):
    r = client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": "gg"
    })

    response = client.get("/gg", follow_redirects=False)

    assert response.status_code == 307


def test_redirect_not_found(client):
    response = client.get("/unknown")

    assert response.json()["error"] == "not found"


def test_delete_link(client):
    client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": "del"
    })

    response = client.delete("/links/del")

    assert response.status_code == 200


def test_delete_not_found(client):
    response = client.delete("/links/unknown")

    assert response.status_code == 404


def test_update_link(client):
    client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": "upd"
    })

    response = client.put("/links/upd", json={
        "original_url": "https://yandex.ru"
    })

    assert response.status_code == 200


def test_update_not_found(client):
    response = client.put("/links/none", json={
        "original_url": "x"
    })

    assert response.status_code == 404


def test_stats(client):
    client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": "stat"
    })

    response = client.get("/links/stat/stats")

    assert response.status_code == 200


def test_stats_not_found(client):
    response = client.get("/links/none/stats")

    assert response.status_code == 404


def test_search(client):
    client.post("/links/shorten", json={
        "original_url": "https://google.com"
    })

    response = client.get("/links/search?original_url=https://google.com")

    assert response.status_code == 200


def test_redirect_increments_click(client):
    client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": "inc"
    })

    client.get("/inc", follow_redirects=False)
    stats = client.get("/links/inc/stats")

    assert stats.json()["clicks"] == 1

