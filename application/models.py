from flask_login import UserMixin
from . import db
from datetime import datetime
from sqlalchemy import text


#Cela semble remplacer le create table

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    roles = db.relationship('Role', secondary='user_roles')
    predictions = db.relationship("Prediction", backref='Users', lazy=True)
    
    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})
        
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


#CRUD




class Prediction(db.Model):
    __tablename__ = 'Predictions'
    id = db.Column(db.Integer, primary_key=True)
    overall = db.Column(db.Integer)
    total_bsmt_sf = db.Column(db.Integer)
    exter = db.Column(db.Integer)
    gr_liv_area = db.Column(db.Integer)
    garage_area = db.Column(db.Integer)
    saleprice_m2_quartier = db.Column(db.Integer)
    totalfullbath = db.Column(db.Integer)
    bsmt = db.Column(db.Integer)
    kitchen_qual = db.Column(db.String(20))
    neighborhood = db.Column(db.String(100))
    estimated_price = db.Column(db.Integer)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



    @classmethod
    def add_prediction(cls, **pred_dict):
        obj=cls(**pred_dict)
        db.session.add(obj)
        db.session.commit()
    
    @classmethod
    def get_prediction_by_user(cls, user_id):
        query = text("""
            SELECT neighborhood,
                   saleprice_m2_quartier,
                   totalfullbath,
                   gr_liv_area, 
                   garage_area,
                   total_bsmt_sf,
                   overall,
                   kitchen_qual,
                   bsmt,
                   exter
            FROM Predictions
            WHERE id_user = :user_id
        """)

        conn = db.session()
        cursor = conn.execute(query, params={"user_id": user_id})
        return cursor.fetchall()
    
    @classmethod
    def delete_last_insert_test(cls):
        conn = db.session()
        conn.execute(''' DELETE FROM Predictions WHERE id=(SELECT Max(id) FROM Predictions)
                              ''')
        db.session.commit()