# routes/nda_soc_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Project
from app.forms import NDASOCForm

nda_soc_bp = Blueprint('nda_soc', __name__)

@nda_soc_bp.route('/nda-soc/<int:project_id>', methods=['GET', 'POST'])
@login_required
def nda_soc(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))

    form = NDASOCForm()

    if request.method == 'POST' and form.validate_on_submit():
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')

        # NDA File Upload
        if form.nda_file.data:
            # Delete old file if exists
            if project.nda_file:
                old_nda_path = os.path.join(upload_folder, project.nda_file)
                if os.path.exists(old_nda_path):
                    os.remove(old_nda_path)
            # Save new file
            nda_filename = secure_filename(form.nda_file.data.filename)
            form.nda_file.data.save(os.path.join(upload_folder, nda_filename))
            project.nda_file = nda_filename

        # SOC File Upload
        if form.soc_file.data:
            # Delete old file if exists
            if project.soc_file:
                old_soc_path = os.path.join(upload_folder, project.soc_file)
                if os.path.exists(old_soc_path):
                    os.remove(old_soc_path)
            # Save new file
            soc_filename = secure_filename(form.soc_file.data.filename)
            form.soc_file.data.save(os.path.join(upload_folder, soc_filename))
            project.soc_file = soc_filename

        project.status = 'NDA & SOC'
        db.session.commit()
        flash('NDA & SOC documents saved successfully.', 'success')
        return redirect(url_for('uo_number.uo_number', project_id=project.id))

    return render_template('nda_soc_form.html', form=form, project=project)
