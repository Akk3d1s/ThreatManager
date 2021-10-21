from app.controllers.report import allowed_file

def test_allowed_file():
    assert allowed_file('xsxx.jpeg') == True
