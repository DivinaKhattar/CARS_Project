# app/models/unique_section.py
from app import db

class UniqueSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    section_code = db.Column(db.String(100), nullable=False)
    project = db.relationship('Project', back_populates='unique_section')
