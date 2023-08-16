import pytest
from app import app
from application.models import User, Prediction
from flask_login import current_user


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client  

def test_predict(client):
    # Connexion to the database
    response = client.post('/login', data={'email': "admin@example.com", "password": "1234"}, follow_redirects=True)
    assert response.request.path == "/profile"



    # Test template
    assert b'<label for="overall">' in response.data
    # Test bad post (null values) 
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_1 = len(predictions)
    response = client.post('/predict', data={'Age_house':None, 'Total Bsmt SF':50, '1st Flr SF':50,
                                             'Gr Liv Area':120,'Garage Area':30, 'Garage Cars':2,
                                             'Overall_Qual':5, 'Bath':2, 'Bsmt Qual':"Good",
                                             'Kitchen Qual': "Excellent", 'Neighborhood': "Crawford"})
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_2 = len(predictions)
    assert length_2 == length_1
    # Test good post
    response = client.post('/predict', data={'Age_house':10, 'Total Bsmt SF':50, '1st Flr SF':50,
                                             'Gr Liv Area':120,'Garage Area':30, 'Garage Cars':2,
                                             'Overall_Qual':5, 'Bath':2, 'Bsmt Qual':"Good",
                                             'Kitchen Qual': "Excellent", 'Neighborhood': "Crawford"})
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_3 = len(predictions)
    assert length_3 == length_2 + 1
    # Test value in template
    assert b'La maison vaut: 69880' in response.data
    # Cleaning of the insertion with the test
    Prediction.delete_last_insert_test()
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_4 = len(predictions)
    assert length_4 == length_2