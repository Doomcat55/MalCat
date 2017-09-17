from myanimelist.models import User


def test_user_name_is_case_insensitive():
    assert User('Doomcat55') == User('doomcat55') == User('DOOMCAT55')
