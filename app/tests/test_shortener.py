from app.utils.shortener import generate_code


def test_generate_code():
    code = generate_code(6)

    assert len(code) == 6
    assert isinstance(code, str)
