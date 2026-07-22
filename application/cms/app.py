from flask import Flask, render_template
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from routes.login import login_bp
from routes.projects import projects_bp
from routes.certifications import certifications_bp
from routes.about import about_bp
from routes.resume import resume_bp

app.register_blueprint(login_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(certifications_bp)
app.register_blueprint(about_bp)
app.register_blueprint(resume_bp)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        # Import models so SQLAlchemy knows about them
        from models.project import Project
        from models.certification import Certification
        from models.site_content import SiteContent
        from models.resume import Resume

        # Create any tables that don't already exist
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)