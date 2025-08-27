from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db, app
from app.models import Project
from app.models.contract import Contract, ContractCostEntry, ContractMilestone
from forms import ContractForm

contract_bp = Blueprint('contract_bp', __name__)

FIXED_COST_CATEGORIES = [
    'Personnel', 'Equipment', 'Travel', 'Contingencies',
    'Visiting Faculty', 'Technical Support', 'IPR Fees', 'Overheads'
]

FIXED_MILESTONES = ['Initial Advance', 'Milestone I', 'Milestone II', 'Final Report']

@contract_bp.route('/contract/<int:project_id>', methods=['GET', 'POST'])
@login_required
def contract(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))

    contract = Contract.query.filter_by(project_id=project.id).first()
    form = ContractForm()

    if request.method == 'GET':
        if contract:
            form.contact_number.data = contract.contact_number
            form.date.data = contract.date
            
            # Load existing cost entries
            for entry in contract.cost_entries:
                form.cost_entries.append_entry({
                    'category': entry.category,
                    'amount': entry.amount
                })

            # Load existing milestones
            for milestone in contract.milestones:
                form.milestones.append_entry({
                    'amount': milestone.amount,
                    'due_date': milestone.due_date
                })
        else:
            # Fresh entries
            for cat in FIXED_COST_CATEGORIES:
                form.cost_entries.append_entry({'category': cat})

            for desc in FIXED_MILESTONES:
                form.milestones.append_entry()

    if form.validate_on_submit():
        if not contract:
            contract = Contract(project_id=project.id)

        contract.contact_number = form.contact_number.data
        contract.date = form.date.data

        # Save PDF
        if form.contract_pdf.data:
            filename = secure_filename(form.contract_pdf.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.contract_pdf.data.save(filepath)
            contract.contract_pdf = filename

        db.session.add(contract)
        db.session.commit()

        # Clear old entries
        ContractCostEntry.query.filter_by(contract_id=contract.id).delete()
        ContractMilestone.query.filter_by(contract_id=contract.id).delete()

        # Save new cost entries
        for entry in form.cost_entries.entries:
            new_entry = ContractCostEntry(
                contract_id=contract.id,
                category=entry.form.category.data,
                amount=entry.form.amount.data
            )
            db.session.add(new_entry)

        # Save new milestones with fixed descriptions if matched
        for idx, milestone in enumerate(form.milestones.entries):
            description = FIXED_MILESTONES[idx] if idx < len(FIXED_MILESTONES) else f"Milestone {idx + 1}"
            new_milestone = ContractMilestone(
                contract_id=contract.id,
                description=description,
                amount=milestone.form.amount.data,
                due_date=milestone.form.due_date.data
            )
            db.session.add(new_milestone)

        project.status = 'CONTRACT'
        db.session.commit()
        flash('Contract details saved successfully.', 'success')
        return redirect(url_for('sanction_letter_bp.sanction_letter', project_id=project.id))

    return render_template('contract.html', form=form, project=project)
