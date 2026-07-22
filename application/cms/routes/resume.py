import os

from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, abort
from werkzeug.utils import secure_filename

from extensions import db
from models.resume import Resume

resume_bp = Blueprint("resume", __name__)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@resume_bp.route("/resume", methods=["GET", "POST"])
def resume():
    resume = Resume.query.first()

    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            return redirect(url_for("resume.resume"))

        if not allowed_file(file.filename):
            return "Only PDF files are allowed.", 400

        upload_dir = os.path.join(current_app.root_path, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        save_path = os.path.join(upload_dir, "resume.pdf")

        if resume is None:
            resume = Resume(filename=secure_filename(file.filename), filepath=save_path)
            db.session.add(resume)
        else:
            resume.filename = secure_filename(file.filename)
            resume.filepath = save_path

        file.save(save_path)
        db.session.commit()

        return redirect(url_for("resume.resume"))

    return render_template("resume.html", resume=resume)


@resume_bp.route("/resume/download")
def download_resume():
    resume = Resume.query.first()

    if resume is None:
        abort(404)

    upload_dir = os.path.join(current_app.root_path, "uploads")

    return send_from_directory(
        upload_dir,
        "resume.pdf",
        as_attachment=True,
        download_name=resume.filename
    )