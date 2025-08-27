# routes/rsqr.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from io import BytesIO
from reportlab.pdfgen import canvas
from app import db
from app.models.project import Project
from app.models.rsqr import RSQR
from app.forms import RSQRForm

rsqr_bp = Blueprint('rsqr', __name__)

@rsqr_bp.route('/rsqr', methods=['GET', 'POST'])
@rsqr_bp.route('/rsqr/<int:project_id>', methods=['GET', 'POST'])
@login_required
def rsqr(project_id=None):
    form = RSQRForm()
    project = None
    rsqr = None

    if project_id:
        project = Project.query.get_or_404(project_id)
        if project.user_id != current_user.id:
            flash('Access denied', 'danger')
            return redirect(url_for('dashboard.dashboard'))

        rsqr = project.rsqr

    if request.method == 'POST':
        if 'update' in request.form:
            flash('Editing enabled. Make changes and click Save.', 'info')

        elif 'save' in request.form and form.validate_on_submit():
            if not project:
                # Create new Project and RSQR together
                project = Project(
                    title=form.title.data,
                    user_id=current_user.id
                )
                db.session.add(project)
                db.session.commit()

            if rsqr:
                rsqr.requirements = form.requirements.data
                rsqr.justification = form.justification.data
                rsqr.deliverables = form.deliverables.data
            else:
                rsqr = RSQR(
                    requirements=form.requirements.data,
                    justification=form.justification.data,
                    deliverables=form.deliverables.data,
                    project_id=project.id
                )
                db.session.add(rsqr)

            db.session.commit()
            flash('RSQR saved successfully.', 'success')
            return redirect(url_for('rsqr.rsqr_success', project_id=project.id))

    if project and rsqr:
        form.title.data = project.title
        form.requirements.data = rsqr.requirements
        form.justification.data = rsqr.justification
        form.deliverables.data = rsqr.deliverables

    return render_template('rsqr.html', form=form, project=project)


@rsqr_bp.route('/rsqr/<int:project_id>/success')
@login_required
def rsqr_success(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('rsqr_success.html', project=project)


@rsqr_bp.route('/rsqr/<int:project_id>/download')
@login_required
def download_rsqr_pdf(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    rsqr = project.rsqr
    if not rsqr:
        flash('RSQR not found.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, f"RSQR Form for Project ID: {project.id}")
    p.drawString(100, 780, f"Title: {project.title}")
    p.drawString(100, 760, f"PI: {project.pi or 'Not yet assigned'}")
    p.drawString(100, 740, f"Institute: {project.institute or 'Not yet assigned'}")
    p.drawString(100, 720, f"Requirements: {rsqr.requirements}")
    p.drawString(100, 700, f"Justification: {rsqr.justification}")
    p.drawString(100, 680, f"Deliverables: {rsqr.deliverables}")

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='rsqr.pdf', mimetype='application/pdf')
