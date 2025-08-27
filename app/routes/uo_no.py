# routes/uo_number_routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Project, UONumber, UOCostEntry

uo_bp = Blueprint('uo', __name__, url_prefix='/uo')

@uo_bp.route('/<int:project_id>', methods=['GET', 'POST'])
@login_required
def uo_number(project_id):
    project = Project.query.get_or_404(project_id)

    # Get or create UONumber entry
    uo = UONumber.query.filter_by(project_id=project.id).first()
    if not uo:
        uo = UONumber(project_id=project.id)
        db.session.add(uo)
        db.session.commit()

    # Fixed categories (always shown)
    fixed_categories = [
        'Personnel', 'Equipment', 'Travel', 'Contingencies',
        'Visiting Faculty', 'Technical Support', 'IPR Fees', 'Overheads'
    ]

    # Lookup for existing entries
    existing_entries = {entry.category: entry for entry in uo.cost_entries}

    if request.method == 'POST':
        mode = request.form.get('mode')

        if mode == 'save':
            # Handle fixed categories
            for category in fixed_categories:
                field_name = f'amount_{category.lower().replace(" ", "_")}'
                amount_str = request.form.get(field_name)
                amount = float(amount_str) if amount_str else 0.0

                if category in existing_entries:
                    existing_entries[category].amount = amount
                else:
                    new_entry = UOCostEntry(
                        uo_number_id=uo.id,
                        category=category,
                        amount=amount
                    )
                    db.session.add(new_entry)

            # Handle dynamic categories
            dynamic_categories = request.form.getlist('dynamic_category[]')
            dynamic_amounts = request.form.getlist('dynamic_amount[]')

            for cat, amt in zip(dynamic_categories, dynamic_amounts):
                category = cat.strip()
                if not category:
                    continue  # Skip empty rows

                try:
                    amount = float(amt)
                except (ValueError, TypeError):
                    amount = 0.0

                if category in existing_entries:
                    existing_entries[category].amount = amount
                else:
                    new_entry = UOCostEntry(
                        uo_number_id=uo.id,
                        category=category,
                        amount=amount
                    )
                    db.session.add(new_entry)

            # Update status and commit all
            project.status = "UO Number Filled"
            db.session.commit()

            return redirect(url_for('uo.uo_success', project_id=project.id))

        elif mode == 'update':
            return render_template('uo_number.html',
                                   project=project,
                                   uo=uo,
                                   categories=fixed_categories,
                                   editable=True)

    return render_template('uo_number.html',
                           project=project,
                           uo=uo,
                           categories=fixed_categories,
                           editable=False)

@uo_bp.route('/success/<int:project_id>')
@login_required
def uo_success(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('uo_success.html', project=project)
