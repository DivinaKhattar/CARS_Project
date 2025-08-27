from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app as app
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from app.models.management_council import ManagementCouncil
from app.forms import ManagementCouncilForm
from werkzeug.utils import secure_filename
import os

management_council_bp = Blueprint('management_council', __name__)

@management_council_bp.route('/management-council/<int:project_id>', methods=['GET', 'POST'])
@login_required
def management_council(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("Access denied", "danger")
        return redirect(url_for('dashboard.dashboard'))

    form = ManagementCouncilForm()
    existing_council = ManagementCouncil.query.filter_by(project_id=project.id).first()

    if form.validate_on_submit():
        if not existing_council:
            existing_council = ManagementCouncil(project_id=project.id)
            db.session.add(existing_council)

        # Fill form data
        existing_council.council_date = form.council_date.data
        existing_council.chairperson = form.chairperson.data
        existing_council.title = form.title.data
        existing_council.pdc = form.pdc.data
        existing_council.cost = form.cost.data

        # Handle PDF upload
        if form.council_pdf.data:
            filename = secure_filename(form.council_pdf.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.council_pdf.data.save(filepath)
            existing_council.council_pdf = filename

        # Update project status
        project.status = 'MANAGEMENT COUNCIL'
        db.session.commit()

        flash('Saved successfully!', 'success')
        return redirect(url_for('management_council.management_council_success', project_id=project.id))

    # Pre-fill form if data exists
    if existing_council:
        form.council_date.data = existing_council.council_date
        form.chairperson.data = existing_council.chairperson
        form.title.data = existing_council.title
        form.pdc.data = existing_council.pdc
        form.cost.data = existing_council.cost

    is_viewing_existing = bool(existing_council and existing_council.council_date)

    return render_template(
        'management_council.html',
        form=form,
        project=project,
        is_viewing_existing=is_viewing_existing
    )
@management_council_bp.route('/management-council/success/<int:project_id>')
@login_required
def management_council_success(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("Access denied", "danger")
        return redirect(url_for('dashboard.dashboard'))

    return render_template('management_success.html', project=project)
