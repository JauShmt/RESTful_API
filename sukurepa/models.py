from sukurepa import db

class tablerinho(db.Model):
    json_id = db.Column(db.Integer, primary_key=True)
    json_objecterinho = db.Column(db.PickleType)
    json_urlerinho = db.Column(db.String(50000))
    json_annoterinho = db.Column(db.Text)