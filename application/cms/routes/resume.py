import os
from io import BytesIO

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    send_file,
)
from werkzeug.utils import secure_filename

from extensions import db
from models.resume import Resume


resume_bp = Blueprint("resume", __name__)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=os.environ.get("AWS_DEFAULT_REGION"),
    )


def get_bucket_name():
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    if not bucket_name:
        raise RuntimeError("S3_BUCKET_NAME is not configured")

    return bucket_name


@resume_bp.route("/resume", methods=["GET", "POST"])
def resume():
    resume = Resume.query.first()

    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            return redirect(url_for("resume.resume"))

        if not allowed_file(file.filename):
            return "Only PDF files are allowed.", 400

        filename = secure_filename(file.filename)

        if not filename:
            return "Invalid filename.", 400

        s3_key = "resume/resume.pdf"

        try:
            s3 = get_s3_client()
            bucket = get_bucket_name()

            s3.upload_fileobj(
                file,
                bucket,
                s3_key,
                ExtraArgs={
                    "ContentType": "application/pdf",
                },
            )
        except (BotoCoreError, ClientError) as exc:
            return f"Resume upload failed: {exc}", 500

        if resume is None:
            resume = Resume(
                filename=filename,
                filepath=s3_key,
            )
            db.session.add(resume)
        else:
            resume.filename = filename
            resume.filepath = s3_key

        db.session.commit()

        return redirect(url_for("resume.resume"))

    return render_template("resume.html", resume=resume)


@resume_bp.route("/resume/download")
def download_resume():
    resume = Resume.query.first()

    if resume is None:
        abort(404)

    try:
        s3 = get_s3_client()
        bucket = get_bucket_name()

        response = s3.get_object(
            Bucket=bucket,
            Key=resume.filepath,
        )

        file_data = response["Body"].read()

        return send_file(
            BytesIO(file_data),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=resume.filename,
        )

    except (BotoCoreError, ClientError):
        abort(404)