from app import db
from sqlalchemy import Numeric

class SummaryOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(Numeric(12, 2))
    gst_amount = db.Column(Numeric(12, 2))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    milestones = db.relationship('MilestoneEntry', backref='summary_offer', cascade='all, delete-orphan')
    cost_entries = db.relationship('CostEntry', backref='summary_offer', cascade='all, delete-orphan')


class MilestoneEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String(100))  # e.g., 'Initial Advance', 'Milestone I', etc.
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    summary_offer_id = db.Column(db.Integer, db.ForeignKey('summary_offer.id'), nullable=False)


class CostEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))  # e.g., 'Personnel', 'Equipment', 'Others'
    amount = db.Column(Numeric(10, 2))
    summary_offer_id = db.Column(db.Integer, db.ForeignKey('summary_offer.id'), nullable=False)
