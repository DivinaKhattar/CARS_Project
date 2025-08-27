# models/project.py
from app import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pi = db.Column(db.String(100), nullable=False)
    institute = db.Column(db.String(200), nullable=False)
    reference_no = db.Column(db.String(50))
    status = db.Column(db.String(50), default='INITIAL STAGE')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships to individual stages
    rsqr = db.relationship('RSQR', uselist=False, backref='project')
    management_council = db.relationship('ManagementCouncil', uselist=False, backref='project')
    offer_evaluation = db.relationship('OfferEvaluation', uselist=False, backref='project')
    summary_offer = db.relationship('SummaryOffer', uselist=False, backref='project')
    nda_soc = db.relationship('NDASOC', back_populates='project', uselist=False, cascade="all, delete-orphan")
    uo_number = db.relationship('UONumber', backref='project', uselist=False, cascade="all, delete-orphan")
   
    unique_section = db.relationship('UniqueSection', back_populates='project', uselist=False)
    contract = db.relationship('Contract', back_populates='project', uselist=False)
