from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models.certification import Certification

certifications_bp = Blueprint("certifications", __name__)

@certifications_bp.route("/certifications")
def certifications():
    certifications = Certification.query.order_by(Certification.id.desc()).all()
    return render_template(
        "certifications.html",
        certifications=certifications
    )

@certifications_bp.route("/certifications/new", methods=["GET", "POST"])
def new_certification():

    if request.method == "POST":

        certification = Certification(
            name=request.form.get("name", ""),
            issuer=request.form.get("issuer", ""),
            credential_url=request.form.get("credential_url", ""),
            status=request.form.get("status", "Active")
        )

        db.session.add(certification)
        db.session.commit()

        return redirect(url_for("certifications.certifications"))

    return render_template("certification_new.html")


@certifications_bp.route("/certifications/<int:certification_id>/edit", methods=["GET", "POST"])
def edit_certification(certification_id):

    certification = Certification.query.get_or_404(certification_id)

    if request.method == "POST":

        certification.name = request.form.get("name", "")
        certification.issuer = request.form.get("issuer", "")
        certification.credential_url = request.form.get("credential_url", "")
        certification.status = request.form.get("status", "Active")

        db.session.commit()

        return redirect(url_for("certifications.certifications"))

    return render_template(
        "certification_edit.html",
        certification=certification
    )


@certifications_bp.route("/certifications/<int:certification_id>/delete", methods=["POST"])
def delete_certification(certification_id):

    certification = Certification.query.get_or_404(certification_id)

    db.session.delete(certification)
    db.session.commit()

    return redirect(url_for("certifications.certifications"))