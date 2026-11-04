from extensions import db

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200), nullable=False)
    credential_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default="Active")

    def __repr__(self):
        return f"<Certification {self.name}>"