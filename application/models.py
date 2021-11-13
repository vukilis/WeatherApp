from application import db

class City(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length=50), nullable = False)