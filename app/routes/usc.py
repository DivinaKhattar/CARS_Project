# app/routes/unique_section_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Project, UniqueSection
from forms import UniqueSectionForm

unique_sanction_bp = Blueprint('unique_section', __name__)

@unique_sanction_bp.route('/unique-section/<int:project_id>', methods=['GET', 'POST'])
@login_required
def unique_section(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('main.dashboard'))

    # Fetch existing entry if it exists
    section = UniqueSection.query.filter_by(project_id=project.id).first()

    # Pre-fill form if already exists
    form = UniqueSectionForm(obj=section)

    if form.validate_on_submit():
        if section:
            # Update existing
            section.section_code = form.section_code.data
        else:
            # Create new
            section = UniqueSection(
                project_id=project.id,
                section_code=form.section_code.data
            )
            db.session.add(section)

        # Optional: update project status
        project.status = 'UNIQUE SECTION'
        db.session.commit()

        flash('Unique Section Code saved successfully.', 'success')
        return redirect(url_for('contract.contract', project_id=project.id))

    return render_template('unique_section.html', form=form, project=project)
