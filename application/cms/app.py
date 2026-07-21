from flask import Flask, render_template
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from routes.login import login_bp
from routes.projects import projects_bp

app.register_blueprint(login_bp)
app.register_blueprint(projects_bp)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)