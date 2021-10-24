# import pytest
# from app import app
# from io import StringIO, BytesIO
# from os.path import join, dirname, realpath

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         with app.app_context():
#             app.config['WTF_CSRF_ENABLED'] = False
#         yield client

# def test_download_threat_file(client):
#     with open(join(dirname(realpath(__file__)))+'/../app/static/uploads/threat2_filename.jpg', 'rb') as file:
#         fileStringIO = BytesIO(file.read())
#     response = client.get('/download_file_threat/2')
#     fileStringIO.seek(0)
#     assert response.headers['Content-Disposition'] == 'attachment; filename=threat2_filename.jpg'