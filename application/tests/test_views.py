# import pytest
# from app import app
# from application.models import User, Prediction
# from flask_login import current_user

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client  
        
# def test_index(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b'<h2 style="font-size:18px"> Bienvenue </h2>' in response.data
    


# def test_login(client):
#     response = client.get('/login')
#     assert response.status_code == 200
#     assert b'<h3 class="title has-text-grey">Espace personnel</h3>' in response.data
#     # Test fake
#     response = client.post('/login', data={'email' : "fake@test.com", 'password' : "fake"}, follow_redirects=True)
#     assert response.request.path == "/signup"
#     assert not hasattr(current_user, "id")
#     # Test ok
#     response = client.post('/login', data={'email': "nounou@test.com", "password": "nounou"}, follow_redirects=True)
#     assert response.request.path == "/predict"
#     assert hasattr(current_user, "id")



# def test_logout(client):
#     client.post('/login', data={'email': "nounou@test.com", "password": "nounou"}, follow_redirects=True)
#     response = client.get('/logout', follow_redirects=True)
#     assert response.status_code == 200
#     assert response.request.path == "/"
#     assert not hasattr(current_user, "id")
   
    

    
# def test_signup(client):
#     response = client.get('/signup')
#     # Test Template
#     assert response.status_code == 200
#     assert b'<h3 class="title has-text-grey">Espace Inscription</h3>' in response.data
#     assert b'<form method="POST" action="/signup" class="form">' in response.data
#     # Test Post With Email already existing
#     length_users_1 = len(User.get_all_user())
#     response = client.post('/signup', data={'email': 'fake@test.com','name':'test', 'password': '123'}, follow_redirects=True)
#     length_users_2 = len(User.get_all_user())
#     assert length_users_2 == length_users_1
#     # Test Post
#     response = client.post('/signup', data={'email': 'nounou@test.com', 'name':'test', 'password': 'nounou'}, follow_redirects=True)
#     length_users_3 = len(User.get_all_user())
#     assert length_users_3 == length_users_2 + 1
#     assert hasattr(current_user, "id")
#     assert response.request.path == '/profile'
