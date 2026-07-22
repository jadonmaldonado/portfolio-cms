from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models.project import Project

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/projects")
def projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template("projects.html", projects=projects)

@projects_bp.route("/projects/new", methods=["GET", "POST"])
def new_project():
    if request.method == "POST":
        project = Project(
            title=request.form.get("title", ""),
            tech_stack=request.form.get("tech_stack", ""),
            github=request.form.get("github", ""),
            live=request.form.get("live", ""),
            description=request.form.get("description", ""),
            featured=request.form.get("featured") == "on",
            status=request.form.get("status", "Draft"),
        )

        db.session.add(project)
        db.session.commit()
        return redirect(url_for("projects.projects"))

    return render_template("project_new.html")

@projects_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        project.title = request.form.get("title", "")
        project.tech_stack = request.form.get("tech_stack", "")
        project.github = request.form.get("github", "")
        project.live = request.form.get("live", "")
        project.description = request.form.get("description", "")
        project.featured = request.form.get("featured") == "on"
        project.status = request.form.get("status", "Draft")

        db.session.commit()
        return redirect(url_for("projects.projects"))

    return render_template("project_edit.html", project=project)

@projects_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("projects.projects"))