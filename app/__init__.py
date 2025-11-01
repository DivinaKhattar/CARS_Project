import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load from config.py (which uses .env)
    from app.config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    scheduler.start()

    # ✅ Safe upload folder handling for Vercel
    upload_folder = app.config.get('UPLOAD_FOLDER', '/tmp/uploads')

    # If running on Vercel, use /tmp (writable)
    if os.environ.get("VERCEL"):
        upload_folder = '/tmp/uploads'

    app.config['UPLOAD_FOLDER'] = upload_folder

    # Create folder safely
    try:
        os.makedirs(upload_folder, exist_ok=True)
    except OSError:
        pass  # ignore read-only errors

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.rsqr import rsqr_bp
    from app.routes.council import management_council_bp
    from app.routes.evalution import offer_bp
    from app.routes.summary import summary_offer_bp
    from app.routes.nda_soc import nda_soc_bp
    from app.routes.uo_no import uo_bp
    from app.routes.usc import unique_sanction_bp
    from app.routes.contract import contract_bp
    from app.routes.sanction import sanction_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(rsqr_bp)
    app.register_blueprint(management_council_bp)
    app.register_blueprint(offer_bp)
    app.register_blueprint(summary_offer_bp)
    app.register_blueprint(nda_soc_bp)
    app.register_blueprint(uo_bp)
    app.register_blueprint(unique_sanction_bp)
    app.register_blueprint(sanction_bp)

    # Scheduled task for daily email alerts
    from app.utils.schedular import check_and_send_due_milestone_alerts
    scheduler.add_job(
        func=check_and_send_due_milestone_alerts,
        trigger='cron',
        hour=0,
        minute=1,
        id='daily_milestone_email_alerts'
    )

    return app
