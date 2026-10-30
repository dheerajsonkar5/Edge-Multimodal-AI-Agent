from database.sqlite import Database


def test_database():

    db = Database()

    assert db is not None

    db.close()