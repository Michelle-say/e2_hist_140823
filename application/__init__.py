from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os
import joblib

# init SQLAlchemy so we can use it later in our models

  
app = Flask(__name__)
db = SQLAlchemy()  

model = joblib.load(open('model/model_nounou.joblib', 'rb'))



app.config['SECRET_KEY'] = 'secret-key-goes-here'
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


#spécifier l' utilisateur loader, Un chargeur d'utilisateurs indique à Flask-Login comment trouver un utilisateur spécifique à partir de l'ID stocké dans son cookie de session.
db.init_app(app)
    

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)




from .models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

