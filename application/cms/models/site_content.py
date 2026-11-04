from extensions import db

class SiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150))
    headline = db.Column(db.String(250))
    about = db.Column(db.Text)

    email = db.Column(db.String(150))
    github = db.Column(db.String(250))
    linkedin = db.Column(db.String(250))

    def __repr__(self):
        return "<SiteContent>"