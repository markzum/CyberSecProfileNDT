from app import create_app


def test_routes_exist():
    app = create_app()
    client = app.test_client()

    for path in ("/", "/intro", "/team"):
        response = client.get(path)
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" in response.data
