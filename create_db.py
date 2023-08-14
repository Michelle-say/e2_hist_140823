from application import db, app
from application.models import User, Role
from werkzeug.security import generate_password_hash


app.app_context().push()
db.create_all() # pass the create_app result so Flask-SQLAlchemy gets the configuration.

new_user = Role(name="User")

db.session.add(new_user)
db.session.commit()


#a voir

if not User.query.filter(User.email == 'admin@example.com').first():
    admin = User(
        email='chichette@example.com',
        password=generate_password_hash('nounou'),
        name='Chichette'
    )
    db.session.add(admin)
    db.session.commit()

if not User.query.filter(User.email == 'user@example.com').first():       
    user = User(
        email="user@example.com",
        password=generate_password_hash('123'),
        name="User"
    )
    user.roles.append(new_user)
    db.session.add(user)
    db.session.commit()