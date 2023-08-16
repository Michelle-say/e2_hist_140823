from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import requests
from . import model
import pandas as pd
from .models import Prediction
from datetime import datetime
from . import db


main =  Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template('home.html')


@main.route('/profile')
@login_required
def profile():
    user_predictions = Prediction.query.filter_by(id_user=current_user.id).all()
    return render_template('profile.html', name=current_user.name, predictions=user_predictions)

@main.route('/prediction_history')
@login_required
def prediction_history():
    user_predictions = Prediction.get_prediction_by_user(current_user.id)
    return render_template('prediction_history.html', predictions=user_predictions)

@main.route('/predict', methods=['GET'])
def predict():
    return render_template('profile.html')


@main.route('/predict', methods=['POST'])
def predict_post():
    X_predict = {}
    for var in ['overall',
                'total_bsmt_sf',
                'exter',
                "gr_liv_area", 
                "garage_area",
                'saleprice_m2_quartier',
                'totalfullbath',
                "kitchen_qual",
                "neighborhood",
                'bsmt']:
        if var in ['neighborhood','kitchen_qual']:
            X_predict[var]= request.form[var]
        else:
            X_predict[var]= float(request.form[var])

    print(X_predict)

    result=int(model.predict(pd.DataFrame(X_predict, index=[0]))[0][0])

    prediction_data = {
        'overall': X_predict['overall'],
        'total_bsmt_sf': X_predict['total_bsmt_sf'],
        'exter': X_predict['exter'],
        "gr_liv_area": X_predict['gr_liv_area'], 
        "garage_area": X_predict['garage_area'],
        'saleprice_m2_quartier': X_predict['saleprice_m2_quartier'],
        'totalfullbath': X_predict['totalfullbath'],
        "kitchen_qual": X_predict['kitchen_qual'],
        "neighborhood": X_predict['neighborhood'],
        'bsmt': X_predict['bsmt'],
        'estimated_price': result,
        'id_user': current_user.id
    }

    Prediction.add_prediction(**prediction_data)
    
    return render_template('profile.html', data=result)