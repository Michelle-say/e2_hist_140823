from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import current_user, login_user, login_required, logout_user
from application import db, app



auth = Blueprint('auth', __name__)



@auth.route('/login')
def login():
    return render_template('login.html')




@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False


    user = User.query.filter_by(email=email).first()

    # check si l'utilisateur existe
    # prend le mot de passe fourni par l'utilisateur, 
    # le hache et le compare au mot de passe haché dans la base de données
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # si la vérification ci-dessus est positive, 
    # nous savons que l'utilisateur a les bonnes informations d'identification
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # valider et ajouter l'utilisateur à la base de données 
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 
    # si cela renvoie un utilisateur, alors l'email existe déjà dans la base de données

    if user: # si un utilisateur est trouvé, il est rediriger vers la page d'inscription pour qu'il puisse réessayer.
       flash("L'adresse email renseignée est déja utilisée")
       return redirect(url_for('auth.signup'))

    # créer un nouvel utilisateur avec les données du formulaire. 
    # Hacher le mot de passe pour que la version en clair ne soit pas sauvegardée.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    return redirect(url_for('main.index'))
