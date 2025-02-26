from app import db

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    umur = db.Column(db.Integer, nullable=False)
    jenis_kelamin = db.Column(db.String(20), nullable=False)