# app/routes/dashboard_routes.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.project import Project
from app.models.rsqr import RSQR
from app.models.management_council import ManagementCouncil
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.created_date.desc()).all()

    for project in projects:
        rsqr_data = RSQR.query.filter_by(project_id=project.id).first()
        council_data = ManagementCouncil.query.filter_by(project_id=project.id).first()
        if rsqr_data and council_data and project.amendment_pdf:
            project.status = "COMPLETE"
        elif rsqr_data and council_data:
            project.status = "ACTIVE"
        elif rsqr_data:
            project.status = "INITIAL STAGE"
        else:
            project.status = "NOT STARTED"

    return render_template('dashboard.html', projects=projects)
