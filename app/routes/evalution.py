# offer_routes.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.project import Project
from app.models.offer_evaluation import OfferEvaluation
from app.forms import OfferEvaluationForm

offer_bp = Blueprint('offer', __name__)
UPLOAD_FOLDER = 'app/static/uploads'  # Make sure this path exists or change as needed


@offer_bp.route('/offer-evaluation/<int:project_id>', methods=['GET', 'POST'])
@login_required
def offer_evaluation(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    form = OfferEvaluationForm()

    # Load existing OfferEvaluation record or create new
    evaluation = OfferEvaluation.query.filter_by(project_id=project_id).first()
    if not evaluation:
        evaluation = OfferEvaluation(project_id=project_id)

    if form.validate_on_submit():
        if form.evaluation_pdf.data:
            filename = secure_filename(form.evaluation_pdf.data.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            form.evaluation_pdf.data.save(filepath)
            evaluation.evaluation_pdf = filename

        evaluation.offer_eval_date = form.offer_eval_date.data
        evaluation.eval_chairperson = form.eval_chairperson.data
        evaluation.eval_member = form.eval_member.data
        evaluation.eval_user = form.eval_user.data

        db.session.add(evaluation)
        project.status = 'OFFER EVALUATION'
        db.session.commit()

        return redirect(url_for('offer.offer_evaluation_success', project_id=project.id))

    # Pre-fill static values for display
    rsqr_title = project.rsqr.title if project.rsqr else ''
    council_date = project.management_council.council_date if project.management_council else ''
    pi_name = project.pi
    institute = project.institute

    # Prefill form if editing
    if evaluation and request.method == 'GET':
        form.offer_eval_date.data = evaluation.offer_eval_date
        form.eval_chairperson.data = evaluation.eval_chairperson
        form.eval_member.data = evaluation.eval_member
        form.eval_user.data = evaluation.eval_user

    return render_template(
        'offer_evaluation.html',
        form=form,
        project=project,
        rsqr_title=rsqr_title,
        council_date=council_date,
        pi_name=pi_name,
        institute=institute,
        is_existing=bool(evaluation and evaluation.offer_eval_date)
    )


@offer_bp.route('/offer-evaluation-success/<int:project_id>')
@login_required
def offer_evaluation_success(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('offer_evaluation_success.html', project=project)
