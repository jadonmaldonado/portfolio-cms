from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models.site_content import SiteContent

about_bp = Blueprint("about", __name__)

@about_bp.route("/about", methods=["GET", "POST"])
def about():

    content = SiteContent.query.first()

    if content is None:
        content = SiteContent()
        db.session.add(content)
        db.session.commit()

    if request.method == "POST":

        content.name = request.form.get("name")
        content.headline = request.form.get("headline")
        content.about = request.form.get("about")
        content.email = request.form.get("email")
        content.github = request.form.get("github")
        content.linkedin = request.form.get("linkedin")

        db.session.commit()

        return redirect(url_for("about.about"))

    return render_template("about.html", content=content)