from app import db
from datetime import datetime

class UONumber(db.Model):
    __tablename__ = 'uo_number'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    uo_number = db.Column(db.String(100), nullable=True)
    total_amount = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Dynamic cost entries (personnel, equipment, etc.)
    cost_entries = db.relationship('UOCostEntry', back_populates='uo_number', cascade="all, delete-orphan")


class UOCostEntry(db.Model):
    __tablename__ = 'uo_cost_entry'

    id = db.Column(db.Integer, primary_key=True)
    uo_number_id = db.Column(db.Integer, db.ForeignKey('uo_number.id'), nullable=False)

    cost_type = db.Column(db.String(255), nullable=False)  # E.g., 'Personnel', 'Travel'
    amount = db.Column(db.Float, nullable=True)

    uo_number = db.relationship('UONumber', back_populates='cost_entries')
