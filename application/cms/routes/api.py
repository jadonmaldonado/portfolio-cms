from flask import Blueprint, jsonify, request


from models.certification import Certification
from models.project import Project
from models.resume import Resume
from models.site_content import SiteContent


api_bp = Blueprint("api", __name__, url_prefix="/api")
@api_bp.after_request
def add_cors_headers(response):
    allowed_origins = {
        "http://localhost:8000",
        "http://jadonmaldonado.com",
        "https://jadonmaldonado.com",
        "https://www.jadonmaldonado.com",
    }

    origin = request.headers.get("Origin")

    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"

    return response

@api_bp.route("/about", methods=["GET"])
def about():
    content = SiteContent.query.first()

    if content is None:
        return jsonify({})

    return jsonify({
        "name": content.name,
        "headline": content.headline,
        "about": content.about,
        "email": content.email,
        "github": content.github,
        "linkedin": content.linkedin,
    })


@api_bp.route("/projects", methods=["GET"])
def projects():
    projects = Project.query.order_by(Project.id.desc()).all()

    return jsonify([
        {
            "id": project.id,
            "title": project.title,
            "tech_stack": project.tech_stack,
            "github": project.github,
            "description": project.description,
            "featured": project.featured,
            "status": project.status,
        }
        for project in projects
    ])


@api_bp.route("/certifications", methods=["GET"])
def certifications():
    certifications = Certification.query.order_by(Certification.id.desc()).all()

    return jsonify([
        {
            "id": certification.id,
            "name": certification.name,
            "issuer": certification.issuer,
            "date_earned": str(certification.date_earned)
            if certification.date_earned
            else None,
            "credential_url": certification.credential_url,
        }
        for certification in certifications
    ])


@api_bp.route("/resume", methods=["GET"])
def resume():
    resume = Resume.query.first()

    if resume is None:
        return jsonify({})

    return jsonify({
        "filename": resume.filename,
        "download_url": "/resume/download",
    })