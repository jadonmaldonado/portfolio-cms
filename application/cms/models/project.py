from extensions import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    tech_stack = db.Column(db.String(250), nullable=False)
    github = db.Column(db.String(500), nullable=False)
    live = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=False)
    featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default="Draft")

    def __repr__(self):
        return f"<Project {self.title}>"