from app import db

class RSQR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requirements = db.Column(db.Text)
    justification = db.Column(db.Text)
    deliverables = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
