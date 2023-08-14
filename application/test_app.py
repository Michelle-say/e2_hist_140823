import pytest
from flask import Flask
from flask.testing import FlaskClient
from application.main import main  # Remplacez 'votre_module_flask' par le nom réel de votre module d'application Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client: FlaskClient):
    response = client.get('/')
    print(response)
    print(response.data)
    assert response.status_code == 200
    assert "Prédiction du prix de la maison" in response.data.decode('utf-8') 


def test_profile(client: FlaskClient):
    response = client.get('/profile')
    assert response.status_code == 302  # Redirection vers la page de connexion car elle nécessite une authentification


def test_predict_get(client: FlaskClient):
    response = client.get('/predict')
    assert response.status_code == 200
    assert "Entrez vos informations" in response.data 


def test_predict_post(client: FlaskClient):
    # Test d'une requête POST à /predict avec des données fictives
    data = {
        'overall': '5',
        'total_bsmt_sf': '1200',
        'exter': '4',
        "gr_liv_area": "1800",
        "garage_area": "400",
        'saleprice_m2_quartier': '112.18',
        'totalfullbath': "2",
        "kitchen_qual": "TA",
        "neighborhood": "Blueste",
        'bsmt': '20'
    }

    response = client.post('/predict', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "Votre prédiction" in response.data  # Remplacez "Votre prédiction" par un contenu de votre template profile.html
