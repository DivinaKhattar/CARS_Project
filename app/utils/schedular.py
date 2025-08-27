# utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from datetime import datetime
from app import db
from app.models.summary_offer import SummaryOfferMilestoneEntry
from app.utils.email import send_email

def check_and_alert_missed_milestones():
    with current_app.app_context():
        today = datetime.today().date()
        milestones = SummaryOfferMilestoneEntry.query.filter(
            SummaryOfferMilestoneEntry.due_date < today,
            SummaryOfferMilestoneEntry.completed == False
        ).all()

        for milestone in milestones:
            project = milestone.summary_offer.project
            user_email = project.user.email
            subject = f"[ALERT] Payment Due: {milestone.milestone_name}"
            body = f"""
Dear {project.user.name},

This is a reminder that the milestone "{milestone.milestone_name}" for project "{project.title}"
was due on {milestone.due_date.strftime('%d %b %Y')} and is still marked as unpaid.

Please take necessary action.

Regards,
CARS System
"""

            send_email(user_email, subject, body)

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_and_alert_missed_milestones, trigger="interval", hours=24)
    scheduler.start()
    print("[SCHEDULER STARTED] Daily email alert for missed payments.")

    # Shut down scheduler when Flask shuts down
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        scheduler.shutdown()
