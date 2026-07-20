from flask import Flask, render_template
from routes.login import login_bp

app = Flask(__name__)
app.register_blueprint(login_bp)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)