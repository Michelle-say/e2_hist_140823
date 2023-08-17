import pytest
from app import app
from application.models import User, Prediction
from flask_login import current_user


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client  




    # Test template
    assert b'<label for="overall">' in response.data
    # Test mauvais post (null values) 
    predictions = Prediction.get_prediction_by_user(current_user.id)
    len_1 = len(predictions)
    response = client.post('/predict', data={'overall':250, 'total_bsmt_sf':100, 'exter':50,
                                             'gr_liv_area':120,'garage_area':30, 'saleprice_m2_quartier':None,
                                             'totalfullbath':5, 'kitchen_qual':'Ex', 'neighborhood':"ClearCr",
                                             'bsmt': "10"})
    predictions = Prediction.get_prediction_by_user(current_user.id)
    len_2 = len(predictions)
    assert len_2 == len_1
    # Test bon post
    response = client.post('/predict', data={'overall':300, 'total_bsmt_sf':50, 'exter':100,
                                             'gr_liv_area':120,'garage_area':30, 'saleprice_m2_quartier':2,
                                             'totalfullbath':5, 'kitchen_qual':'Po', 'neighborhood':"Blueste",
                                             'bsmt': "20"})
    predictions = Prediction.get_prediction_by_user(current_user.id)
    len_3 = len(predictions)
    assert len_3 == len_2 + 1
    # Test value in template
    assert b'La maison vaut: 69880' in response.data
    # Cleaning of the insertion with the test
    Prediction.delete_last_insert_test()
    predictions = Prediction.get_prediction_by_user(current_user.id)
    len_4 = len(predictions)
    assert len_4 == len_2