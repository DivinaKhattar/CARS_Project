from app import db

class ManagementCouncil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    council_date = db.Column(db.Date)
    council_pdf = db.Column(db.String(200))
    chairperson = db.Column(db.String(100))
    pdc = db.Column(db.String(100))
    cost = db.Column(db.Float)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
