from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
from app.models import Project, SummaryOffer, SummaryOfferCostEntry, SummaryOfferMilestoneEntry
from app.forms import SummaryOfferForm
from app.utils.email import send_email_reminder

summary_offer_bp = Blueprint('summary_offer', __name__)

@summary_offer_bp.route('/summary-offer/<int:project_id>', methods=['GET', 'POST'])
@login_required
def summary_offer(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash("Access denied", "danger")
        return redirect(url_for("dashboard"))

    form = SummaryOfferForm()

    existing_offer = SummaryOffer.query.filter_by(project_id=project.id).first()
    is_editing = existing_offer is not None

    if request.method == 'POST':
        if not existing_offer:
            summary_offer = SummaryOffer(project_id=project.id)
        else:
            summary_offer = existing_offer
            # Clear old entries
            SummaryOfferCostEntry.query.filter_by(summary_offer_id=summary_offer.id).delete()
            SummaryOfferMilestoneEntry.query.filter_by(summary_offer_id=summary_offer.id).delete()

        # Save cost entries
        subtotal = 0
        for index in range(len(request.form.getlist('cost_type[]'))):
            cost_type = request.form.getlist('cost_type[]')[index]
            cost_amount = float(request.form.getlist('cost_amount[]')[index])
            subtotal += cost_amount
            cost_entry = SummaryOfferCostEntry(
                summary_offer=summary_offer,
                cost_type=cost_type,
                amount=cost_amount
            )
            db.session.add(cost_entry)

        summary_offer.gst_amount = round(subtotal * 0.18, 2)
        summary_offer.total_amount = round(subtotal + summary_offer.gst_amount, 2)

        # Save milestones
        for index in range(len(request.form.getlist('milestone_name[]'))):
            name = request.form.getlist('milestone_name[]')[index]
            amount = float(request.form.getlist('milestone_amount[]')[index])
            date = datetime.strptime(request.form.getlist('milestone_date[]')[index], "%Y-%m-%d")
            milestone_entry = SummaryOfferMilestoneEntry(
                summary_offer=summary_offer,
                milestone_name=name,
                amount=amount,
                due_date=date
            )
            db.session.add(milestone_entry)

        # Handle PDF
        if 'summary_pdf' in request.files:
            pdf_file = request.files['summary_pdf']
            if pdf_file and pdf_file.filename != '':
                filename = secure_filename(pdf_file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                pdf_file.save(filepath)
                summary_offer.pdf_filename = filename

        # Save and commit
        db.session.add(summary_offer)
        project.status = "SUMMARY OFFER"
        db.session.commit()

        flash("Summary Offer saved successfully!", "success")
        return redirect(url_for("summary_offer.summary_offer_success", project_id=project.id))

    return render_template(
        "summary_offer.html",
        form=form,
        project=project,
        existing_offer=existing_offer
    )


@summary_offer_bp.route('/summary-offer-success/<int:project_id>')
@login_required
def summary_offer_success(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('summary_offer_success.html', project=project)
