from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db, app
from app.models import Project
from app.models.sanction import SanctionLetter, SanctionCostEntry, SanctionScheduleEntry, SanctionCARSEntry
from forms import SanctionLetterForm

sanction_bp = Blueprint('sanction', __name__)

@sanction_bp.route('/sanction-letter/<int:project_id>', methods=['GET', 'POST'])
@login_required
def sanction_letter(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))

    sanction = SanctionLetter.query.filter_by(project_id=project_id).first()
    form = SanctionLetterForm()

    if form.validate_on_submit():
        if not sanction:
            sanction = SanctionLetter(project_id=project_id)

        sanction.contact_number = form.contact_number.data
        sanction.date = form.date.data

        # Save PDF
        if form.sanction_pdf.data:
            filename = secure_filename(form.sanction_pdf.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.sanction_pdf.data.save(filepath)
            sanction.sanction_pdf = filename

        # Clear previous entries
        sanction.costs.clear()
        sanction.schedule_milestones.clear()
        sanction.cars_milestones.clear()

        # Save cost entries
        for entry in form.cost_entries.data:
            sanction.costs.append(SanctionCostEntry(category=entry['category'], amount=entry['amount']))

        # Save schedule
        for entry in form.schedule_entries.data:
            sanction.schedule_milestones.append(SanctionScheduleEntry(date=entry['date'], amount=entry['amount']))

        # Save CARS milestones
        for entry in form.cars_entries.data:
            sanction.cars_milestones.append(SanctionCARSEntry(
                milestone_description=entry['milestone_description'],
                deliverables=entry['deliverables'],
                duration_months=entry['duration_months']
            ))

        project.status = 'COMPLETE'
        db.session.add(sanction)
        db.session.commit()

        flash('Sanction Letter saved successfully!', 'success')
        return redirect(url_for('dashboard'))

    elif request.method == 'GET' and sanction:
        form.contact_number.data = sanction.contact_number
        form.date.data = sanction.date

        for cost in sanction.costs:
            form.cost_entries.append_entry({
                'category': cost.category,
                'amount': cost.amount
            })
        for sch in sanction.schedule_milestones:
            form.schedule_entries.append_entry({
                'date': sch.date,
                'amount': sch.amount
            })
        for cars in sanction.cars_milestones:
            form.cars_entries.append_entry({
                'milestone_description': cars.milestone_description,
                'deliverables': cars.deliverables,
                'duration_months': cars.duration_months
            })

    return render_template('sanction_letter.html', form=form, project=project, sanction=sanction)
